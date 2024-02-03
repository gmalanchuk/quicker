from fastapi.requests import Request

from src.exceptions import LoginRequiredException


async def get_access_token(request: Request) -> dict:
    access_token = request.session.get("access_token")
    if not access_token:
        raise LoginRequiredException
    return access_token


async def get_refresh_token(request: Request) -> dict:
    refresh_token = request.session.get("refresh_token")
    if not refresh_token:
        raise LoginRequiredException
    return refresh_token
