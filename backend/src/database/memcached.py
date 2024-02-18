from pymemcache.client.base import Client

from src.config import settings


# create a connection to Memcached
client = Client((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
