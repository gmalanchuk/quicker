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

    async def __get_track_title_with_artists(self, request: Request, spotify_track_reference: str) -> str:
        spotify_client = await self.spotify_client.get_client(request=request)

        information_about_track = spotify_client.track(spotify_track_reference)
        track_title = information_about_track["name"]
        track_artists = ", ".join(
            [artist["name"] for artist in information_about_track["artists"]]
        )  # to display songwriters in commas, like: 'Clonnex, irlbabee'
        track_title_with_artists = f"{track_artists} - {track_title}"  # 'Clonnex, irlbabee - Mova Kokhannia'

        return track_title_with_artists

    @staticmethod
    async def __get_track_location(track_title_with_artists: str) -> str:
        """Returns the location of the track on the server.
        For example, 'music/Clonnex, irlbabee - Mova Kokhannia.mp3'"""
        track_location = f"{settings.DO_SPACES_MUSIC_FOLDER_NAME}/{track_title_with_artists}.mp3"
        return track_location

    async def download_track(
        self, spotify_track_reference_in_request: TrackReferenceRequestSchema, request: Request
    ) -> TrackReferenceResponseSchema:
        # doesn't work with this song https://open.spotify.com/track/2Lhdl74nwwVGOE2Gv35QuK?si=6bf63852fa6746a4

        spotify_track_reference = spotify_track_reference_in_request.model_dump()["track_reference"]

        track_title_with_artists = await self.__get_track_title_with_artists(
            request=request, spotify_track_reference=spotify_track_reference
        )  # 'Clonnex, irlbabee - Mova Kokhannia'
        track_location = await self.__get_track_location(
            track_title_with_artists=track_title_with_artists
        )  # 'music/Clonnex, irlbabee - Mova Kokhannia.mp3'

        track_exists = await self.do_spaces.check_if_track_exists(track_title_with_artists)
        if track_exists:
            track_reference_on_digital_ocean_spaces = await self.do_spaces.get_track(track_title_with_artists)
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
