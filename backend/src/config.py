import boto3
from pydantic_settings import BaseSettings
from spotipy import SpotifyOAuth


class Settings(BaseSettings):
    """Loading environments from the .env file"""

    SESSION_SECRET_KEY: str

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_SCOPE: str

    DO_SPACES_REGION_NAME: str
    DO_SPACES_ENDPOINT_URL: str
    DO_SPACES_ACCESS_KEY: str
    DO_SPACES_SECRET_KEY: str
    DO_SPACES_MUSIC_FOLDER_NAME: str

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

# DIGITAL OCEAN SPACES
digital_ocean_spaces = boto3.client(
    "s3",
    region_name=settings.DO_SPACES_REGION_NAME,
    endpoint_url=settings.DO_SPACES_ENDPOINT_URL,
    aws_access_key_id=settings.DO_SPACES_ACCESS_KEY,
    aws_secret_access_key=settings.DO_SPACES_SECRET_KEY,
)
