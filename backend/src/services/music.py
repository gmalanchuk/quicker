import os

from fastapi.requests import Request
from pytube import Search, YouTube

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.repositories.memcached import MemcachedRepository
from src.services.utils.digital_ocean_spaces import DigitalOceanSpaces
from src.services.utils.spotify import SpotifyClient


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()
        self.memcached = MemcachedRepository()

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        # TODO if / in the track title, then replace it with a space

        track_title_with_mp3 = await self.spotify_client.get_track_title_with_mp3(
            request=request, spotify_track_reference=spotify_track_reference
        )  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        # check if the track exists in the memcached
        track_reference = await self.memcached.get_one(key=track_title_with_mp3)
        if track_reference:
            return TrackReferenceResponseSchema(track_reference=track_reference)

        youtube_track_reference = Search(track_title_with_mp3).results[0].watch_url

        # TODO create a separate thread for downloading music
        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_title_with_mp3)  # download the track on the server
        # TODO ----------------------------------------------

        # upload the track to the DO spaces and get the reference to it
        track_reference_on_digital_ocean_spaces = await self.do_spaces.upload_track_and_link_back_to_it(
            track_title_with_mp3=track_title_with_mp3
        )

        os.remove(track_title_with_mp3)  # remove the track from the server

        # add the track to the memcached
        await self.memcached.add_one(key=track_title_with_mp3, value=track_reference_on_digital_ocean_spaces)

        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
