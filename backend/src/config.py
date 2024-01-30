from pydantic_settings import BaseSettings
from spotipy import SpotifyOAuth


class Settings(BaseSettings):
    """Loading environments from the .env file"""

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_SCOPE: str

    SESSION_SECRET_KEY: str

    class Config:
        env_file = ".env"


# ENVIRONMENT VARIABLES
settings = Settings()

# SPOTIFY AUTHENTICATION
spotify_oauth = SpotifyOAuth(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIFY_REDIRECT_URI,
    scope=settings.SPOTIFY_SCOPE,
)
