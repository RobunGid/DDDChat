from aiogram import Bot, F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from aiogram_i18n import I18nContext
from containers.factories import get_container
from exceptions.chats import ChatMessageCreateTimeoutRequestException, ChatMessageCreateWebException
from handlers.converters.chats import convert_chat_dtos_to_translated_message
from services.chats import ChatsStorageService
from services.web import BaseChatWebService

chats_router = Router(name="Chats")


@chats_router.message(Command("chats"))
async def get_chats_handler(message: Message, i18n: I18nContext):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chats = await service.get_all_chats()
        chat_string = convert_chat_dtos_to_translated_message(chats, i18n)
        if chat_string != "":
            await message.answer(chat_string)
        else:
            await message.answer(
                i18n.get(
                    "chats_not_found",
                ),
            )


@chats_router.message(F.chat.is_forum, F.message_thread_id.is_not(None), F.content_type == ContentType.TEXT)
async def send_message_to_chat_handler(
    message: Message,
):
    container = get_container()

    async with container() as request_container:
        web_service = await request_container.get(BaseChatWebService)
        storage_service = await request_container.get(ChatsStorageService)
        chat_data = await storage_service.get_chat_data_by_telegram_id(telegram_chat_id=str(message.message_thread_id))

        await web_service.create_message_in_chat(chat_oid=chat_data.web_chat_id, message_text=message.html_text)


@chats_router.error(ExceptionTypeFilter(ChatMessageCreateTimeoutRequestException), F.update.message.as_("message"))
async def handle_timeout_exception(event: ErrorEvent, message: Message, bot: Bot, i18n: I18nContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=i18n.get("message_create_fail_timeout"),
        message_thread_id=message.message_thread_id,
    )


# TODO: catch status codess
@chats_router.error(ExceptionTypeFilter(ChatMessageCreateWebException), F.update.message.as_("message"))
async def handle_web_response_exception(event: ErrorEvent, message: Message, bot: Bot, i18n: I18nContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=i18n.get("message_create_fail_response"),
        message_thread_id=message.message_thread_id,
    )
