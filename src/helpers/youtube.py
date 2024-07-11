import yt_dlp
from loguru import logger
from youtubesearchpython import VideosSearch


class YoutubeClient:
    @staticmethod
    def download_track(track_name: str) -> bool:
        track = VideosSearch(track_name, limit=1).result()["result"][0]

        track_url = track["link"]

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": track_name[:-4],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([track_url])
            logger.info(f"Track {track_name} has been downloaded successfully")
