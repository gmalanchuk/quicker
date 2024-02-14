import os

from fastapi.requests import Request
from pytube import Search, YouTube

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.services.utils.digital_ocean_spaces import DigitalOceanSpaces
from src.services.utils.spotify import SpotifyClient


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        # TODO if / in the track title, then replace it with a space

        track_title_with_mp3 = await self.spotify_client.get_track_title_with_mp3(
            request=request, spotify_track_reference=spotify_track_reference
        )  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        # TODO create database for tracks and check if the track exists in the database
        track_reference_on_digital_ocean_spaces = await self.do_spaces.check_if_track_exists_and_return_it(
            track_title_with_mp3=track_title_with_mp3
        )
        if track_reference_on_digital_ocean_spaces:  # check if the track exists in DO Spaces otherwise download it
            return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
        # TODO ------------------------------------------------------------------------

        youtube_track_reference = Search(track_title_with_mp3).results[0].watch_url

        # TODO create a separate thread for downloading music
        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_title_with_mp3)  # download the track on the server
        # TODO ----------------------------------------------

        # upload the track to the DO spaces
        await self.do_spaces.upload_track(track_title_with_mp3=track_title_with_mp3)

        os.remove(track_title_with_mp3)  # remove the track from the server

        # get a link to a track that has just been uploaded to DO Spaces
        track_reference_on_digital_ocean_spaces = await self.do_spaces.get_track(track_title_with_mp3)
        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
