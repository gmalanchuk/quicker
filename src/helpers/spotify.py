from spotipy import Spotify, SpotifyClientCredentials

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


class SpotifyBaseClient:
    @staticmethod
    async def get_spotify_client() -> Spotify:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        return Spotify(auth_manager=auth_manager)


class SpotifyClient(SpotifyBaseClient):
    async def get_track_name(self, track_link: str) -> str:
        # todo сделать более красивый вывод названия трека
        spotify_client = await self.get_spotify_client()

        information_about_track = spotify_client.track(track_link)
        track_name = information_about_track["name"]  # 'Mova Kokhannia'

        print(track_name)

        # replace '/' with '*' in the track name because '/' is not allowed in a file name and is treated as a directory
        if "/" in track_name:
            track_name = track_name.replace("/", "*")

        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'

        track_name = f"{track_artists} - {track_name}.mp3"  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        return track_name
