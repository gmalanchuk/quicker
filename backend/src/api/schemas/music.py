from typing import NoReturn, Union

from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from starlette import status


class TrackReferenceRequestSchema(BaseModel):
    track_reference: str

    @field_validator("track_reference")
    def validate_track_reference(cls, track_reference: str) -> Union[str, NoReturn]:
        if "https://open.spotify.com/track/" not in track_reference:
            raise HTTPException(detail="Invalid Spotify track link", status_code=status.HTTP_400_BAD_REQUEST)
        return track_reference


class TrackReferenceResponseSchema(BaseModel):
    track_reference: str
