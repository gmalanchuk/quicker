from aiogram.types import FSInputFile, Message
from loguru import logger

from main import bot
from services.music import MusicService


async def music_handler(message: Message) -> None:
    # todo docstring

    link = message.text

    if "track" in link:
        logger.info(f"Start downloading track by link: {link}")
        track_name = await MusicService().download_track(track_link=link)
        audio_file = FSInputFile(track_name)
        await bot.send_audio(chat_id=message.chat.id, audio=audio_file)
    else:
        logger.info(f"User {message.from_user.full_name} sent a message with an invalid link: {link}")
        await message.reply("Something went wrong. Please, check the link and try again")
