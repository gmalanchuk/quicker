import os

from fastapi import APIRouter, Request
from pytube import Search, YouTube
from spotipy import Spotify, SpotifyException

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.config import digital_ocean_spaces, settings
from src.exceptions import TokenExpiredException
from src.get_jwt_tokens import get_access_token


music_router = APIRouter(prefix="/v1/music", tags=["Music"])


async def get_spotify_client(request: Request) -> Spotify:
    access_token = await get_access_token(request=request)

    spotify_client = Spotify(auth=access_token)
    try:
        spotify_client.current_user()
    except SpotifyException:
        raise TokenExpiredException

    return spotify_client


@music_router.post(path="/track/")
async def download_track(
    spotify_track_reference_in_request: TrackReferenceRequestSchema,
    request: Request,
) -> TrackReferenceResponseSchema:
    """Download the track from Spotify, upload it
    to Digital Ocean Spaces and return the track link"""

    spotify_client = await get_spotify_client(request=request)

    spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]
    information_about_track = spotify_client.track(spotify_track_reference)

    track_name = information_about_track["name"]
    track_artists = ", ".join(
        [artist["name"] for artist in information_about_track["artists"]]
    )  # to display songwriters in commas, like: 'Clonnex, irlbabee'

    # track filename and location on the server, like: 'music/Clonnex, irlbabee - Mova Kokhannia.mp3', where 'music'
    # is a directory and 'Clonnex, irlbabee - Mova Kokhannia.mp3' is a filename in this directory
    track_location_and_filename = f"music/{track_artists} - {track_name}.mp3"

    # TODO add a check for the existence of a track on Digital Ocean Spaces and return a link to track if it exists

    youtube_track_reference = Search(f"{track_name} {track_artists}").results[0].watch_url

    # TODO create a separate thread for downloading music
    track = YouTube(youtube_track_reference)
    stream = track.streams.filter(only_audio=True).first()
    stream.download(filename=track_location_and_filename)
    # TODO ----------------------------------------------

    with open(track_location_and_filename, "rb") as downloaded_track:
        digital_ocean_spaces.upload_fileobj(
            Fileobj=downloaded_track,  # track which will be uploaded to Digital Ocean Spaces
            Bucket="music",  # name of the directory in Digital Ocean Spaces
            Key=f"{track_artists} - {track_name}.mp3",  # name of the track
            ExtraArgs={"ACL": "public-read"},  # make the file public
        )

    os.remove(track_location_and_filename)  # remove the track from the server

    track_reference_on_digital_ocean_spaces = f"{settings.DO_SPACES_ENDPOINT_URL}/{track_location_and_filename}"
    return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)


# @music_router.post(path="/playlist/")
# async def download_tracks_from_playlist():
#     pass
