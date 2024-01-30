import spotipy
from fastapi import APIRouter, Request, status
from spotipy import SpotifyOAuth
from starlette.responses import RedirectResponse, JSONResponse

from src.config import settings

music_router = APIRouter(prefix="/v1/music", tags=["Music"])


sp_oauth = SpotifyOAuth(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIFY_REDIRECT_URI,
    scope=settings.SPOTIFY_SCOPE,
    show_dialog=True,
)


@music_router.get("/login/")
async def spotify_login():
    redirect_uri = sp_oauth.get_authorize_url()
    return RedirectResponse(redirect_uri)


@music_router.get("/callback/")
async def callback(request: Request):
    code_in_query_params = request.query_params["code"]
    information_about_token = sp_oauth.get_access_token(code_in_query_params)

    access_token = information_about_token["access_token"]
    request.session["access_token"] = access_token

    return JSONResponse(content={'access_token': access_token}, status_code=status.HTTP_200_OK)


@music_router.post("/")
async def get_information_about_song_by_reference(song_reference: str, request: Request):
    access_token = request.session["access_token"]

    client = spotipy.Spotify(auth=access_token)

    track = client.track(song_reference)

    track_name = track["name"]
    track_artists = [artist["name"] for artist in track["artists"]]
    track_cover_art_url = track["album"]["images"][0]["url"]

    return JSONResponse(
        {'track_name': track_name, 'track_artists': track_artists, 'track_cover_art_url': track_cover_art_url})
