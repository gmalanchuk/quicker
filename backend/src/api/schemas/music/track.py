from typing import NoReturn, Union

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class TrackLinkRequestSchema(BaseModel):
    track_link: str

    @field_validator("track_link")
    def validate_track_link(cls, track_link: str) -> Union[str, NoReturn]:
        if "https://open.spotify.com/track/" not in track_link:
            raise HTTPException(detail="Invalid Spotify track link", status_code=status.HTTP_400_BAD_REQUEST)
        return track_link


class TrackLinkResponseSchema(BaseModel):
    track_link: str
