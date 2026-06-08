from aiogram import Bot
from consumers.schemas import DeleteChatSchema, NewChatMessageSchema, NewChatSchema
from containers.factories import get_container
from faststream import Context
from faststream.kafka.broker import KafkaRouter
from services.chats import ChatsStorageService

from settings.config import get_config

config = get_config()

router = KafkaRouter()


@router.subscriber(config.new_message_received_event_topic, group_id=config.kafka_group_id)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
    key: bytes = Context("message.raw_message.key"),
):
    container = get_container()
    async with container() as request_container:
        storage_service = await request_container.get(ChatsStorageService)
        chat_data = await storage_service.get_chat_data_by_web_chat_id(web_chat_id=message.chat_oid)

        bot = await request_container.get(Bot)
        await bot.send_message(
            chat_id=config.telegram_support_group_id,
            text=message.message_text,
            message_thread_id=int(chat_data.telegram_chat_id),
        )


@router.subscriber(config.chats_deleted_event_topic, group_id=config.kafka_group_id)
async def chat_deleted_subscription_handler(data: DeleteChatSchema):
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        storage_service = await request_container.get(ChatsStorageService)
        chat_data = await storage_service.get_chat_data_by_web_chat_id(web_chat_id=data.chat_oid)
        await bot.delete_forum_topic(
            chat_id=config.telegram_support_group_id,
            message_thread_id=int(chat_data.telegram_chat_id),
        )
        await storage_service.delete_chat_by_telegram_chat_id(telegram_chat_id=chat_data.telegram_chat_id)


@router.subscriber(config.new_chats_event_topic, group_id=config.kafka_group_id)
async def new_chat_subscription_handler(data: NewChatSchema):
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chats_service = await request_container.get(ChatsStorageService)
        topic_name = data.chat_title
        forum_topic = await bot.create_forum_topic(chat_id=config.telegram_support_group_id, name=topic_name)
        await chats_service.add_chat(telegram_chat_id=str(forum_topic.message_thread_id), web_chat_id=data.chat_oid)
