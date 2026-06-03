import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings.config import Config

config = Config()
bot = Bot(token=config.tg_bot_token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply("Hi")


@dp.message()
async def echo(message: Message):
    await message.reply(str(message.text))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    bot = Bot(token=config.tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main())
