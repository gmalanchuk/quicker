import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from src.config import BOT_TOKEN


dp = Dispatcher()


async def main():
    bot = Bot(token=BOT_TOKEN)

    await dp.start_polling(bot)
    logger.info("Bot started")


if __name__ == "__main__":
    asyncio.run(main())
