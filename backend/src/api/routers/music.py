from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request

from src.api.schemas.music.playlist import PlaylistLinkRequestSchema
from src.api.schemas.music.track import TrackLinkRequestSchema, TrackLinkResponseSchema
from src.services.music import MusicService


music_router = APIRouter(prefix="/v1/music", tags=["Music"])


@music_router.post(path="/track/")
async def download_track(
    request: Request,
    spotify_track_link: TrackLinkRequestSchema,
    music_service: Annotated[MusicService, Depends()],
) -> TrackLinkResponseSchema:
    """Download the track from Spotify, upload it
    to Digital Ocean Spaces and return the track link"""

    return await music_service.download_track(
        spotify_track_link=spotify_track_link,
        request=request,
    )


@music_router.post(path="/playlist/")
async def download_playlist_tracks(
    request: Request,
    spotify_playlist_link: PlaylistLinkRequestSchema,
    music_service: Annotated[MusicService, Depends()],
) -> None:
    """Download tracks from playlist, upload them to
    Digital Ocean Spaces and return the track links"""

    return await music_service.download_playlist_tracks(
        spotify_playlist_link=spotify_playlist_link,
        request=request,
    )
