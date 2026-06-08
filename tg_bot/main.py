import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from handlers.base import base_router
from handlers.chats import chats_router
from repositories.initialize import create_tables

from settings.config import get_config

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

i18n_middleware = I18nMiddleware(core=FluentRuntimeCore(path="locales/{locale}"))

config = get_config()
dp = Dispatcher()
bot = Bot(token=config.tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


dp.include_router(base_router)
dp.include_router(chats_router)

dp.message.middleware(i18n_middleware)
i18n_middleware.setup(dispatcher=dp)


async def main():
    create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
