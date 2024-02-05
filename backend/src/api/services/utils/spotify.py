from fastapi.requests import Request
from spotipy import Spotify, SpotifyException

from src.api.services.utils.exceptions import TokenExpiredException
from src.api.services.utils.get_jwt_tokens import GetJWTTokens


class SpotifyClient:
    def __init__(self) -> None:
        self.jwt = GetJWTTokens()

    async def get_client(self, request: Request) -> Spotify:
        access_token = await self.jwt.get_access_token(request=request)
        spotify_client = Spotify(auth=access_token)

        try:
            spotify_client.current_user()  # check if the token is valid
        except SpotifyException:
            raise TokenExpiredException

        return spotify_client
