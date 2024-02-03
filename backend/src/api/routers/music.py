from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.api.services.music import MusicService


music_router = APIRouter(prefix="/v1/music", tags=["Music"])


@music_router.post(path="/track/")
async def download_track(
    spotify_track_reference_in_request: TrackReferenceRequestSchema,
    request: Request,
    music_service: Annotated[MusicService, Depends()],
) -> TrackReferenceResponseSchema:
    """Download the track from Spotify, upload it
    to Digital Ocean Spaces and return the track link"""

    return await music_service.download_track(
        spotify_track_reference_in_request=spotify_track_reference_in_request,
        request=request,
    )
