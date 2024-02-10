from fastapi.requests import Request
from spotipy import Spotify, SpotifyException

from src.services.utils.exceptions import TokenExpiredException
from src.services.utils.get_jwt_tokens import GetJWTTokens


class SpotifyClient:
    def __init__(self) -> None:
        self.jwt = GetJWTTokens()

    async def get_track_title_with_artists(self, request: Request, spotify_track_reference: str) -> str:
        spotify_client = await self.__get_spotify_client(request=request)

        information_about_track = spotify_client.track(spotify_track_reference)
        track_title = information_about_track["name"]
        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'
        track_title_with_artists = f"{track_artists} - {track_title}"  # 'Clonnex, irlbabee - Mova Kokhannia'

        return track_title_with_artists

    async def __get_spotify_client(self, request: Request) -> Spotify:
        access_token = await self.jwt.get_access_token(request=request)  # get an access token from the session
        spotify_client = Spotify(auth=access_token)

        try:
            spotify_client.current_user()  # check if the token is valid
        except SpotifyException:
            raise TokenExpiredException

        return spotify_client
