import spotipy
from aiogram.types import Message
from spotipy.oauth2 import SpotifyClientCredentials

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


async def handle_message(message: Message):
    # Аутентификация
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    information_about_track = sp.track(message.text)

    track_name = information_about_track["name"]  # 'Mova Kokhannia'

    # replace '/' with '*' in the track name because '/' is not allowed in a file name and is treated as a directory
    if "/" in track_name:
        track_name = track_name.replace("/", "*")

    track_artists = ", ".join(
        [artist["name"] for artist in information_about_track["artists"]]
    )  # to display songwriters in commas, like: 'Clonnex, irlbabee'

    track_title_with_mp3 = f"{track_artists} - {track_name}.mp3"  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

    print(track_title_with_mp3)

    await message.reply(track_title_with_mp3)
