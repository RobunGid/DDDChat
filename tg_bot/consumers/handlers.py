from aiogram import Bot
from faststream.kafka.broker import KafkaRouter

from consumers.schemas import DeleteChatSchema, NewChatMessageSchema, NewChatSchema
from containers.factories import get_container
from services.chats_storage import ChatsStorageService
from settings.config import get_config

config = get_config()

router = KafkaRouter()


@router.subscriber(config.message_create_event_topic, group_id=config.kafka_group_id)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
):
    container = get_container()
    async with container() as request_container:
        storage_service = await request_container.get(ChatsStorageService)
        chat_mapping_data = await storage_service.get_chat_mapping_data_by_web_chat_id(web_chat_id=message.chat_oid)

        bot = await request_container.get(Bot)
        await bot.send_message(
            chat_id=config.telegram_support_group_id,
            text=message.message_text,
            message_thread_id=int(chat_mapping_data.telegram_thread_id),
        )


@router.subscriber(config.chat_delete_event_topic, group_id=config.kafka_group_id)
async def chat_deleted_subscription_handler(data: DeleteChatSchema):
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        storage_service = await request_container.get(ChatsStorageService)
        chat_mapping_data = await storage_service.get_chat_mapping_data_by_web_chat_id(web_chat_id=data.chat_oid)
        await bot.delete_forum_topic(
            chat_id=config.telegram_support_group_id,
            message_thread_id=int(chat_mapping_data.telegram_thread_id),
        )
        await storage_service.delete_chat_mapping_data_by_telegram_thread_id(
            telegram_thread_id=chat_mapping_data.telegram_thread_id,
        )


@router.subscriber(config.chat_create_event_topic, group_id=config.kafka_group_id)
async def new_chat_subscription_handler(data: NewChatSchema):
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chats_service = await request_container.get(ChatsStorageService)
        topic_name = data.chat_title
        forum_topic = await bot.create_forum_topic(chat_id=config.telegram_support_group_id, name=topic_name)
        await chats_service.add_chat_mapping_data(
            telegram_thread_id=str(forum_topic.message_thread_id),
            web_chat_id=data.chat_oid,
        )
