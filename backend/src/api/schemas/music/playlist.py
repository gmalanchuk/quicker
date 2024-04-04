from typing import NoReturn, Union

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class PlaylistLinkRequestSchema(BaseModel):
    playlist_link: str

    @field_validator("playlist_link")
    def validate_playlist_link(cls, playlist_link: str) -> Union[str, NoReturn]:
        if "https://open.spotify.com/playlist/" not in playlist_link:
            raise HTTPException(detail="Invalid Spotify playlist link", status_code=status.HTTP_400_BAD_REQUEST)
        return playlist_link
