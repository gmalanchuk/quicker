import asyncio
import os
from threading import Thread

from fastapi.requests import Request

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.repositories.memcached import MemcachedRepository
from src.services.utils.digital_ocean_spaces import DigitalOceanSpaces
from src.services.utils.spotify import SpotifyClient
from src.services.utils.youtube import YoutubeClient


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()
        self.youtube_client = YoutubeClient()
        self.memcached = MemcachedRepository()

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        track_title_with_mp3 = await self.spotify_client.get_track_title_with_mp3(
            request=request, spotify_track_reference=spotify_track_reference
        )  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        # check if the track exists in the memcached and return it if it does
        track_reference = await self.memcached.get_one(key=track_title_with_mp3)
        if track_reference:
            return TrackReferenceResponseSchema(track_reference=track_reference)

        # download the track from the YouTube and save it on the server
        track_download_thread = Thread(target=self.youtube_client.download_track, args=(track_title_with_mp3,))
        track_download_thread.start()
        while track_download_thread.is_alive():
            await asyncio.sleep(1)

        # upload the track to the DO spaces and get the reference to it
        track_reference_on_digital_ocean_spaces = await self.do_spaces.upload_track_and_link_back_to_it(
            track_title_with_mp3=track_title_with_mp3
        )

        os.remove(track_title_with_mp3)  # remove the track from the server

        # add the track to the memcached
        await self.memcached.add_one(key=track_title_with_mp3, value=track_reference_on_digital_ocean_spaces)

        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
