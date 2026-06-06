from typing import cast

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message
from aiogram_i18n import I18nContext
from containers.factories import get_container
from exceptions.chats import ListenerAddRequestException
from handlers.converters.chats import convert_chat_dtos_to_translated_message
from services.web import BaseChatWebService

chats_router = Router(name="Base")


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


@chats_router.message(Command("add_chat"))
async def add_chat_handler(message: Message, i18n: I18nContext, command: CommandObject, state: FSMContext):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        if not command.args:
            await message.answer(
                i18n.get(
                    "add_chat_need_argument",
                ),
            )
            return

        await service.add_listener(telegram_chat_id=str(message.chat.id), chat_oid=command.args)

        await message.answer(
            i18n.get(
                "add_chat_success",
            ),
        )


@chats_router.message(F.chat.is_forum, F.message_thread_id.is_not(None))
async def send_message_to_chat_handler(
    message: Message,
    # state: FSMContext,
    # i18n: I18nContext,
):
    await message.answer(text=f"Message sent to {message.message_thread_id}")


@chats_router.error(ExceptionTypeFilter(ListenerAddRequestException), F.update.message.as_("message"))
async def add_chat_exception_handler(
    event: ErrorEvent[ListenerAddRequestException],
    i18n: I18nContext,
    message: Message,
):
    exc = cast(ListenerAddRequestException, event.exception)
    if exc.status_code == 409:
        await message.answer(
            i18n.get(
                "add_chat_already_connected_fail",
            ),
        )
    elif exc.status_code == 404:
        await message.answer(
            i18n.get(
                "add_chat_not_found_fail",
            ),
        )
