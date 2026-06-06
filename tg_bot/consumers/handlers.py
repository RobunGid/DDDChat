from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from consumers.schemas import ChatMessageSchema, ChatSchema
from containers.factories import get_container
from faststream import Context
from faststream.kafka.broker import KafkaRouter
from services.web import BaseChatWebService

from settings.config import get_config

config = get_config()

router = KafkaRouter()


@router.subscriber(config.new_message_received_event_topic, group_id=config.kafka_group_id)
async def new_message_subscription_handler(message: ChatMessageSchema, key: bytes = Context("message.raw_message.key")):
    container = get_container()
    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        listeners = await service.get_chat_listeners(chat_oid=key.decode())
        chat_data = await service.get_chat_data(chat_oid=key.decode())

        bot = await request_container.get(Bot)

        for listener in listeners:
            await bot.send_message(
                chat_id=listener.oid,
                text=f"{chat_data.format_to_html()}\n\n<pre>{message.message_text}</pre>",
                parse_mode=ParseMode.HTML,
            )


@router.subscriber(config.new_chats_event_topic, group_id=config.kafka_group_id)
async def new_chat_subscription_handler(chat: ChatSchema, key: bytes = Context("message.raw_message.key")):
    # TODO: save telegram thread id and map it to chat_oid
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        topic_name = f"{chat.chat_title} | {chat.chat_oid}"
        await bot.create_forum_topic(chat_id=config.telegram_support_group_id, name=topic_name)
