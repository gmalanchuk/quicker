from pydantic import BaseModel, HttpUrl


class TrackReferenceRequestSchema(BaseModel):
    track_reference: HttpUrl


class TrackReferenceResponseSchema(BaseModel):
    track_reference: str
