from abc import ABC, abstractmethod
from typing import NoReturn


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one(self, *args: tuple, **kwargs: dict) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, *args: tuple, **kwargs: dict) -> NoReturn:
        raise NotImplementedError
