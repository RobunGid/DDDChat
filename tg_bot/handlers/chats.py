from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from containers.factories import get_container
from handlers.converters.chats import convert_chat_dtos_to_translated_message
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
    i18n: I18nContext,
):
    await message.answer(text=f"{message.message_thread_id}")
