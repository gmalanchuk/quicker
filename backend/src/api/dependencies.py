from src.api.routers.auth import auth_router
from src.api.routers.music import music_router


all_api_routers = (music_router, auth_router)
