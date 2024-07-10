import os

from dotenv import load_dotenv
from loguru import logger


# ENVIRONMENT VARIABLES
load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


# LOGGING
logger.add("debug.log", format="{time} | {level} | {message}", level="DEBUG")
