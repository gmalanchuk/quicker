import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from loguru import logger

from config import TELEGRAM_BOT_TOKEN


dispatcher = Dispatcher()


def event_handlers_registration() -> None:
    from handlers.start import get_start
    from handlers.track import handle_message

    #  TODO возможно стоит создать dependencies файл
    dispatcher.message.register(get_start, Command(commands=["start"]))
    dispatcher.message.register(handle_message)


async def main(start_time: datetime) -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Registration of event handlers
    event_handlers_registration()

    logger.info(f"Bot started. Startup time: {datetime.now() - start_time}")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    start_time = datetime.now()
    logger.info("Bot is starting...")

    try:
        asyncio.run(main(start_time))
    except KeyboardInterrupt:
        logger.info(f"Bot stopped. Time of work: {datetime.now() - start_time}")
