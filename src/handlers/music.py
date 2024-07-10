from aiogram.types import Message

from services.music import MusicService


async def music_handler(message: Message):
    track_link = message.text

    # TODO если трек, то вызывается этот метод, если плейлист, то другой
    track_name = await MusicService().download_track(track_link=track_link)

    await message.reply(track_name)
