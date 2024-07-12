from helpers.clients.spotify import SpotifyClient
from helpers.clients.youtube import YoutubeClient


class MusicService:
    def __init__(self) -> None:
        self.spotify_client = SpotifyClient()
        self.youtube_client = YoutubeClient()

    async def download_track(self, track_name_with_mp3: str) -> None:
        self.youtube_client.download_track(track_name_with_mp3)

        # download the track from the YouTube and save it on the server
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     future = executor.submit(self.youtube_client.download_track, track_name)
        #     while future.running():
        #         await asyncio.sleep(0.1)  # wait until the track is downloaded
        #     if future.result():  # result is True if the track is age-restricted
        #         pass  # todo подумать как можно вернуть ошибку
