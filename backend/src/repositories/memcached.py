from src.config import memcached_client, settings
from src.repositories.abstract import AbstractRepository


class MemcachedRepository(AbstractRepository):
    async def __call__(self, *args: tuple, **kwargs: dict) -> None:  # authenticate the memcached client
        await memcached_client.auth(settings.MEMCACHED_USERNAME, settings.MEMCACHED_PASSWORD)

    async def get_one(self, key: str) -> str:
        key = "".join(key.split())  # remove spaces from the key
        return await memcached_client.get(key=key.encode())  # get value by byte key

    async def add_one(self, key: str, value: str) -> None:
        key = "".join(key.split())  # remove spaces from the key
        await memcached_client.set(key=key.encode(), value=value.encode())  # set value and key as bytes
