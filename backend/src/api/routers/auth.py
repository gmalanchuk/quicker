from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse, RedirectResponse

from src.config import spotify_oauth
from src.get_jwt_tokens import get_refresh_token


auth_router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@auth_router.get("/login/spotify/")
async def spotify_login() -> RedirectResponse:
    spotify_redirect_uri = spotify_oauth.get_authorize_url()
    return RedirectResponse(spotify_redirect_uri)


@auth_router.get("/callback/spotify/")
async def spotify_callback(request: Request) -> JSONResponse:
    code_in_query_params = request.query_params["code"]
    information_about_token = spotify_oauth.get_access_token(code_in_query_params)

    access_token = information_about_token["access_token"]
    refresh_token = information_about_token["refresh_token"]

    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token

    return JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/jwt/refresh/")
async def update_access_and_refresh_tokens(request: Request) -> JSONResponse:
    refresh_token = await get_refresh_token(request=request)

    new_access_token = spotify_oauth.refresh_access_token(refresh_token=refresh_token)["access_token"]

    request.session["access_token"] = new_access_token

    return JSONResponse(content={"access_token": new_access_token}, status_code=status.HTTP_200_OK)
