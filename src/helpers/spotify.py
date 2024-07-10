from spotipy import Spotify, SpotifyClientCredentials

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


class SpotifyBaseClient:
    @staticmethod
    async def get_spotify_client() -> Spotify:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        return Spotify(auth_manager=auth_manager)


class SpotifyClient(SpotifyBaseClient):
    async def get_track_name(self, track_link: str) -> str:
        spotify_client = await self.get_spotify_client()

        information_about_track = spotify_client.track(track_link)
        track_name = information_about_track["name"]  # 'Mova Kokhannia'

        track_artist = information_about_track["artists"][0]["name"]  # 'Clonnex'

        # replace '/' with '*' in the track name because '/' is not allowed in a file name and is treated as a directory
        if "/" in track_name:
            track_name = track_name.replace("/", "*")

        full_track_name = f"{track_artist} - {track_name}.mp3"  # 'Clonnex - Mova Kokhannia.mp3'

        return full_track_name
