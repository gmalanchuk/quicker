from fastapi import APIRouter, Request, status
from starlette.responses import RedirectResponse, JSONResponse

from src.config import spotify_oauth

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
    request.session["access_token"] = access_token

    return JSONResponse(content={'access_token': access_token}, status_code=status.HTTP_200_OK)
