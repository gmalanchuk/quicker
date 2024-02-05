import os

from fastapi.requests import Request
from pytube import Search, YouTube

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.api.services.utils.digital_ocean_spaces import DigitalOceanSpaces
from src.api.services.utils.spotify import SpotifyClient
from src.config import settings


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        # doesn't work with this song https://open.spotify.com/track/2Lhdl74nwwVGOE2Gv35QuK?si=6bf63852fa6746a4

        spotify_client = await self.spotify_client.get_client(request=request)

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

        track_reference_on_digital_ocean_spaces = await self.do_spaces.get_track(track_title_with_artists)
        if track_reference_on_digital_ocean_spaces:
            return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)

        youtube_track_reference = Search(track_title_with_artists).results[0].watch_url

        # TODO create a separate thread for downloading music
        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_location_and_filename)
        # TODO ----------------------------------------------

        await self.do_spaces.upload_track(track_location_and_filename)

        os.remove(track_location_and_filename)  # remove the track from the server

        track_reference_on_digital_ocean_spaces = f"{settings.DO_SPACES_ENDPOINT_URL}/{track_location_and_filename}"
        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
