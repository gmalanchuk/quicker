import os

from dotenv import load_dotenv
from loguru import logger

# ENVIRONMENT VARIABLES
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# LOGGING
logger.add("debug.log", format="{time} | {level} | {message}", level="DEBUG")
