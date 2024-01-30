from pydantic_settings import BaseSettings


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
