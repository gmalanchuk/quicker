import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from loguru import logger

from config import TELEGRAM_BOT_TOKEN


dispatcher = Dispatcher()
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def handlers_registration() -> None:
    from handlers.music import music_handler
    from handlers.start import start_handler

    dispatcher.message.register(start_handler, Command(commands=["start"]))
    dispatcher.message.register(music_handler)


async def main(bot_start_time: datetime) -> None:
    # Register handlers
    handlers_registration()

    logger.info(f"Bot started. Startup time: {datetime.now() - bot_start_time}")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    bot_start_time = datetime.now()
    logger.info("Bot is starting...")

    try:
        asyncio.run(main(bot_start_time))
    except KeyboardInterrupt:
        logger.info(f"Bot stopped. Time of work: {datetime.now() - bot_start_time}")
