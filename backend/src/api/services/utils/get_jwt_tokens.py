from typing import Literal

from fastapi.requests import Request

from src.api.services.utils.exceptions import LoginRequiredException


class GetJWTTokens:
    @staticmethod
    async def __get_token(token_type: Literal["access", "refresh"], request: Request) -> str:
        tokens = {
            "access": request.session.get("access_token"),
            "refresh": request.session.get("refresh_token"),
        }

        token = tokens[token_type]

        if not token:
            raise LoginRequiredException
        return token

    async def get_access_token(self, request: Request) -> str:
        return await self.__get_token(token_type="access", request=request)

    async def get_refresh_token(self, request: Request) -> str:
        return await self.__get_token(token_type="refresh", request=request)
