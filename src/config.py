import os

from dotenv import load_dotenv
from loguru import logger

logger.remove()
logger.add("application.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
