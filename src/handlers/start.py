from aiogram.filters import CommandStart
from aiogram.types import Message

from main import dispatcher


@dispatcher.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {message.from_user.full_name}")
