import os

from fastapi.requests import Request
from pytube import Search, YouTube

from src.api.schemas.music import TrackReferenceRequestSchema, TrackReferenceResponseSchema
from src.config import settings
from src.services.utils.digital_ocean_spaces import DigitalOceanSpaces
from src.services.utils.spotify import SpotifyClient


class MusicService:
    def __init__(self) -> None:
        self.do_spaces = DigitalOceanSpaces()
        self.spotify_client = SpotifyClient()

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        # doesn't work with this song https://open.spotify.com/track/2Lhdl74nwwVGOE2Gv35QuK?si=6bf63852fa6746a4

        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        # 'Clonnex, irlbabee - Mova Kokhannia'
        track_title_with_artists = await self.spotify_client.get_track_title_with_artists(
            request=request, spotify_track_reference=spotify_track_reference
        )
        # 'music/Clonnex, irlbabee - Mova Kokhannia.mp3'
        track_location = f"{settings.DO_SPACES_MUSIC_FOLDER_NAME}/{track_title_with_artists}.mp3"

        track_reference_on_digital_ocean_spaces = await self.do_spaces.check_if_track_exists_and_return_it(
            track_title_with_artists=track_title_with_artists
        )
        if track_reference_on_digital_ocean_spaces:  # check if the track exists in DO Spaces otherwise download it
            return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)

        youtube_track_reference = Search(track_title_with_artists).results[0].watch_url

        # TODO create a separate thread for downloading music
        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_location)  # download the track from YouTube
        # TODO ----------------------------------------------

        await self.do_spaces.upload_track(track_location)  # upload the track to the DO spaces

        os.remove(track_location)  # remove the track from the server

        # get a link to a track that has just been uploaded to DO Spaces
        track_reference_on_digital_ocean_spaces = await self.do_spaces.get_track(track_title_with_artists)
        return TrackReferenceResponseSchema(track_reference=track_reference_on_digital_ocean_spaces)
