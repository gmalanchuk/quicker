import os

import spotipy
from fastapi import APIRouter, Request
from pytube import YouTube, Search

from src.api.schemas.music import TrackReferenceSchema
from src.config import digital_ocean_spaces, settings

music_router = APIRouter(prefix="/v1/music", tags=["Music"])


@music_router.post(path="/")
async def get_information_about_track_by_reference(
        spotify_track_reference_in_request: TrackReferenceSchema, request: Request
) -> None:
    # TODO separate this code into a separate function
    access_token = request.session["access_token"]
    spotify_client = spotipy.Spotify(auth=access_token)
    # TODO -------------------------------------------

    spotify_track_reference = str(spotify_track_reference_in_request.model_dump()["track_reference"])
    information_about_track = spotify_client.track(spotify_track_reference)

    track_name = information_about_track["name"]
    track_artists = ', '.join(
        [artist["name"] for artist in information_about_track["artists"]]
    )  # for a beautiful display of music authors, like: 'Justin Hurwitz, Li Jun Li'
    track_filename = f"music/{track_artists} - {track_name}.mp3"  # track name and location on the server

    youtube_track_reference = Search(f'{track_name} {track_artists}').results[0].watch_url

    # TODO create a separate thread for downloading music
    track = YouTube(youtube_track_reference)
    stream = track.streams.filter(only_audio=True).first()
    stream.download(filename=track_filename)
    # TODO ----------------------------------------------

    with open(track_filename, 'rb') as downloaded_track:
        digital_ocean_spaces.upload_fileobj(
            Fileobj=downloaded_track,  # track which will be uploaded to DO Spaces
            Bucket='music',  # name of the directory in DO Spaces
            Key=f'{track_artists} - {track_name}.mp3',  # name of the track
            ExtraArgs={'ACL': 'public-read'},  # make the file public
        )

    os.remove(track_filename)  # remove the track from the server

    return None
