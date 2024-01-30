import spotipy
from fastapi import APIRouter, Request

from src.api.schemas.music import TrackInformationSchema, TrackReferenceSchema


music_router = APIRouter(prefix="/v1/music", tags=["Music"])


@music_router.post(path="/", response_model=TrackInformationSchema)
async def get_information_about_track_by_reference(
        track_reference: TrackReferenceSchema, request: Request
) -> TrackInformationSchema:
    access_token = request.session["access_token"]
    spotify_client = spotipy.Spotify(auth=access_token)

    track_reference = str(track_reference.model_dump()["track_reference"])
    information_about_track = spotify_client.track(track_reference)

    track_name = information_about_track["name"]
    track_artists = [artist["name"] for artist in information_about_track["artists"]]
    track_cover_art_url = information_about_track["album"]["images"][0]["url"]

    return TrackInformationSchema(
        track_name=track_name,
        track_artists=track_artists,
        track_cover_art_url=track_cover_art_url
    )
