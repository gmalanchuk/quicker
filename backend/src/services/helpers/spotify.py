from fastapi.requests import Request
from spotipy import Spotify, SpotifyException

from src.services.helpers.exceptions import TokenExpiredException
from src.services.helpers.get_jwt_tokens import JWT


class SpotifyBaseClient:
    def __init__(self) -> None:
        self.jwt = JWT()

    async def get_spotify_client(self, request: Request) -> Spotify:
        access_token = await self.jwt.get_access_token(request=request)  # get an access token from the session
        spotify_client = Spotify(auth=access_token)

        try:
            spotify_client.current_user()  # check if the access token is valid
        except SpotifyException:
            raise TokenExpiredException

        return spotify_client


class SpotifyClient(SpotifyBaseClient):
    async def get_track_title_with_mp3(self, request: Request, spotify_track_link: str) -> str:
        spotify_client = await self.get_spotify_client(request=request)

        information_about_track = spotify_client.track(spotify_track_link)

        track_name = information_about_track["name"]  # 'Mova Kokhannia'

        # replace '/' with '*' in the track name because '/' is not allowed in a file name and is treated as a directory
        if "/" in track_name:
            track_name = track_name.replace("/", "*")

        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'

        track_title_with_mp3 = f"{track_artists} - {track_name}.mp3"  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        return track_title_with_mp3
