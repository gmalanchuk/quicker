import os

import yt_dlp
from loguru import logger
from youtubesearchpython import VideosSearch

from config import DOWNLOAD_FOLDER


class YoutubeClient:
    @staticmethod
    def download_track(track_name_with_mp3: str) -> bool:
        track = VideosSearch(track_name_with_mp3, limit=1).result()["result"][0]
        track_url = track["link"]

        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, track_name_with_mp3[:-4]),  # Save in 'downloads' folder
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([track_url])
            logger.info(f"Track {track_name_with_mp3} has been downloaded successfully")
