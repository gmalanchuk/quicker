from aiogram.filters import CommandStart
from aiogram.types import Message

from src.main import dispatcher


@dispatcher.message(CommandStart())
async def get_start(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {message.from_user.full_name}")
