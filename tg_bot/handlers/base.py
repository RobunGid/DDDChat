from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

base_router = Router(name="Base")


@base_router.message(CommandStart())
async def start_handler(message: Message, i18n: I18nContext):
    welcome_name = message.from_user.full_name if message.from_user and message.from_user.full_name else ""
    await message.reply(i18n.get("start", name=welcome_name))


@base_router.message(Command("help"))
async def help_handler(message: Message, i18n: I18nContext):
    await message.reply(
        i18n.get(
            "help",
        ),
    )
