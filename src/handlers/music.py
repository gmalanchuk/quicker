import os

from aiogram.types import FSInputFile, Message
from loguru import logger

from config import DOWNLOAD_FOLDER
from helpers.clients.spotify import SpotifyClient
from main import bot
from services.music import MusicService


async def music_handler(message: Message) -> None:
    # todo docstring

    link = message.text

    if "track" in link:
        logger.info(f"Start downloading track by link: {link}")

        track_name_with_mp3 = await SpotifyClient().get_track_name(link)  # 'Clonnex - Mova Kokhannia.mp3'

        track_path = os.path.join(DOWNLOAD_FOLDER, track_name_with_mp3)
        if not os.path.exists(track_path):
            await MusicService().download_track(track_name_with_mp3)

        audio_file = FSInputFile(track_path)
        await bot.send_audio(chat_id=message.chat.id, audio=audio_file)  # todo чтобы отвечал на сообщение

    else:
        logger.info(f"User {message.from_user.full_name} sent a message with an invalid link: {link}")
        await message.reply("Something went wrong. Please, check the link and try again")
