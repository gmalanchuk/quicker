import os

from fastapi.requests import Request
from pytube import Search, YouTube
from spotipy import Spotify, SpotifyException

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.api.services.utils.exceptions import TokenExpiredException
from src.api.services.utils.get_jwt_tokens import GetJWTTokens
from src.config import digital_ocean_spaces, settings


class MusicService:
    def __init__(self) -> None:
        self.jwt = GetJWTTokens()

    async def get_spotify_client(self, request: Request) -> Spotify:
        access_token = await self.jwt.get_access_token(request=request)
        spotify_client = Spotify(auth=access_token)

        try:
            spotify_client.current_user()
        except SpotifyException:
            raise TokenExpiredException

        return spotify_client

    # TODO create a class for working with Digital Ocean Spaces
    @staticmethod
    async def upload_track_to_digital_ocean_spaces(track_location_and_filename: str) -> None:
        # directory_name = 'music', track_title_with_artists = 'Clonnex, irlbabee - Mova Kokhannia.mp3'
        directory_name, track_title_with_artists = track_location_and_filename.split("/")
        with open(track_location_and_filename, "rb") as downloaded_track:
            digital_ocean_spaces.upload_fileobj(
                Fileobj=downloaded_track,  # track which will be uploaded to Digital Ocean Spaces
                Bucket=directory_name,  # name of the directory in Digital Ocean Spaces
                Key=track_title_with_artists,  # name of the track
                ExtraArgs={"ACL": "public-read"},  # make the file public
            )

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        spotify_client = await self.get_spotify_client(request=request)

        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        # TODO separate the code for getting information about the track into a separate method
        information_about_track = spotify_client.track(spotify_track_reference)
        track_title = information_about_track["name"]
        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'
        track_title_with_artists = f"{track_artists} - {track_title}"

        # track filename and location on the server, like: 'music/Clonnex, irlbabee - Mova Kokhannia.mp3', where 'music'
        # is a directory and 'Clonnex, irlbabee - Mova Kokhannia.mp3' is a filename in this directory
        track_location_and_filename = f"music/{track_title_with_artists}.mp3"
        # TODO --------------------------------------------------------------------------------

        # TODO add a check for the existence of a track on Digital Ocean Spaces and return a link to track if it exists

        youtube_track_reference = Search(track_title_with_artists).results[0].watch_url

        # TODO create a separate thread for downloading music
        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_location_and_filename)
        # TODO ----------------------------------------------

        await self.upload_track_to_digital_ocean_spaces(track_location_and_filename)

        os.remove(track_location_and_filename)  # remove the track from the server

        track_reference_on_digital_ocean_spaces = f"{settings.DO_SPACES_ENDPOINT_URL}/{track_location_and_filename}"
        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
