import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from fastapi.requests import Request

from src.api.schemas.music.playlist import PlaylistLinkRequestSchema
from src.api.schemas.music.track import TrackLinkRequestSchema, TrackLinkResponseSchema
from src.repositories.memcached import MemcachedRepository
from src.services.helpers.digital_ocean_spaces import DigitalOceanSpaces
from src.services.helpers.exceptions import AgeRestrictedException
from src.services.helpers.spotify import SpotifyClient
from src.services.helpers.youtube import YoutubeClient


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()
        self.youtube_client = YoutubeClient()
        self.memcached = MemcachedRepository()

    async def download_track(
        self, spotify_track_link: TrackLinkRequestSchema, request: Request
    ) -> TrackLinkResponseSchema:
        track_title_with_mp3 = await self.spotify_client.get_track_title_with_mp3(
            request=request, spotify_track_link=spotify_track_link.track_link
        )  # 'Clonnex, irlbabee - Mova Kokhannia.mp3'

        # check if the track exists in the memcached and return it if it does
        track_link = await self.memcached.get_one(key=track_title_with_mp3)
        if track_link:
            return TrackLinkResponseSchema(track_link=track_link)

        # download the track from the YouTube and save it on the server
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.youtube_client.download_track, track_title_with_mp3)
            while future.running():
                await asyncio.sleep(0.1)  # wait until the track is downloaded
            if future.result():  # result is True if the track is age-restricted
                raise AgeRestrictedException

        # upload the track to the DO spaces and get the link to it
        track_link_on_digital_ocean_spaces = await self.do_spaces.upload_track_and_link_back_to_it(
            track_title_with_mp3=track_title_with_mp3
        )

        os.remove(track_title_with_mp3)  # remove the track from the server

        # add the track to the memcached
        await self.memcached.add_one(key=track_title_with_mp3, value=track_link_on_digital_ocean_spaces)

        return TrackLinkResponseSchema(track_link=track_link_on_digital_ocean_spaces)

    async def download_playlist_tracks(
        self, spotify_playlist_link: PlaylistLinkRequestSchema, request: Request
    ) -> None:
        pass
