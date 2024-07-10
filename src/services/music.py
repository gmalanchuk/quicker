from helpers.spotify import SpotifyClient


class MusicService:
    def __init__(self) -> None:
        self.spotify_client = SpotifyClient()

    async def download_track(self, track_link: str) -> str:
        track_name = await self.spotify_client.get_track_name(track_link)
        return track_name
