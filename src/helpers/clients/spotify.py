from spotipy import Spotify, SpotifyClientCredentials

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from helpers.track_name_cleaner import TrackNameCleaner


class SpotifyBaseClient:
    @staticmethod
    async def get_spotify_client() -> Spotify:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        return Spotify(auth_manager=auth_manager)


class SpotifyClient(SpotifyBaseClient):
    def __init__(self):
        self.track_name_cleaner = TrackNameCleaner()

    async def get_track_name(self, track_link: str) -> str:
        spotify_client = await self.get_spotify_client()

        information_about_track = spotify_client.track(track_link)
        track_name = information_about_track["name"]  # 'Mova Kokhannia'
        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'

        # 'Clonnex - Mova Kokhannia'
        track_name_with_mp3 = await self.track_name_cleaner.get_cleaned_track_name(track_name, track_artists)

        return track_name_with_mp3
