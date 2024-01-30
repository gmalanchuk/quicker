from pydantic import BaseModel, HttpUrl


class TrackReferenceSchema(BaseModel):
    track_reference: HttpUrl


class TrackInformationSchema(BaseModel):
    track_name: str
    track_artists: list[str]
    track_cover_art_url: str
