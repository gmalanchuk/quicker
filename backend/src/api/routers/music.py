import spotipy
from fastapi import APIRouter, Request
from pytube import YouTube, Search

from src.api.schemas.music import TrackReferenceSchema


music_router = APIRouter(prefix="/v1/music", tags=["Music"])


@music_router.post(path="/")
async def get_information_about_track_by_reference(
        spotify_track_reference_in_request: TrackReferenceSchema, request: Request
) -> None:
    # todo separate this code into a separate function
    access_token = request.session["access_token"]
    spotify_client = spotipy.Spotify(auth=access_token)
    # todo -------------------------------------------

    spotify_track_reference = str(spotify_track_reference_in_request.model_dump()["track_reference"])
    information_about_track = spotify_client.track(spotify_track_reference)

    track_name = information_about_track["name"]
    track_artists = ', '.join(
        [artist["name"] for artist in information_about_track["artists"]]
    )  # for a beautiful display of music authors, like: 'Justin Hurwitz, Li Jun Li'

    youtube_track_reference = Search(f'{track_name} {track_artists}').results[0].watch_url

    track = YouTube(youtube_track_reference)
    stream = track.streams.filter(only_audio=True).first()
    stream.download(filename=f"{track_artists} - {track_name}.mp3", output_path="music")

    # TODO create storage for all mp3 files on DO Spaces and return to users only link,
    #  which will start automatic download of file

    return None
