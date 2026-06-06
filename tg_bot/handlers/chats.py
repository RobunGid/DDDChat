import re
from typing import cast

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ErrorEvent, Message
from aiogram_i18n import I18nContext
from containers.factories import get_container
from exceptions.chats import ListenerAddRequestException
from handlers.converters.chats import convert_chat_dtos_to_translated_message
from services.web import BaseChatWebService

chats_router = Router(name="Base")


class MessageFormState(StatesGroup):
    reply = State()


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


@chats_router.message(Command("start_dialog"))
async def start_dialog_handler(message: Message, i18n: I18nContext, command: CommandObject, state: FSMContext):
    await message.answer(
        i18n.get(
            "start_dialog_success",
        ),
    )

    await state.set_state(MessageFormState.reply)


@chats_router.message(MessageFormState.reply)
async def send_message_to_chat_handler(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
):
    if message.reply_to_message is None or message.reply_to_message.text is None:
        await message.answer(
            i18n.get(
                "send_message_fail_not_reply",
            ),
        )
        return
    match_chat_oid = re.search(
        r"🆔\s*<code>([0-9a-fA-F-]{36})</code>",
        message.reply_to_message.html_text,
    )
    if not match_chat_oid:
        await message.answer(
            i18n.get(
                "send_message_fail_oid_not_found",
            ),
        )
        return

    chat_oid = match_chat_oid.group(1).strip()
    await message.answer(f"Message sent to {chat_oid}")
    await state.set_state(MessageFormState.reply)


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
