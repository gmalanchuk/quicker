from helpers.spotify import SpotifyClient
from helpers.youtube import YoutubeClient


class MusicService:
    def __init__(self) -> None:
        self.spotify_client = SpotifyClient()
        self.youtube_client = YoutubeClient()

    async def download_track(self, track_link: str) -> str:
        track_name = await self.spotify_client.get_track_name(track_link)  # 'Clonnex - Mova Kokhannia.mp3'

        self.youtube_client.download_track(track_name)

        # download the track from the YouTube and save it on the server
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     future = executor.submit(self.youtube_client.download_track, track_name)
        #     while future.running():
        #         await asyncio.sleep(0.1)  # wait until the track is downloaded
        #     if future.result():  # result is True if the track is age-restricted
        #         pass  # todo подумать как можно вернуть ошибку

        return track_name
