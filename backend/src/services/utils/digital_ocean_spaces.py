from typing import Union

from botocore.exceptions import ClientError

from src.config import digital_ocean_spaces, settings


class DigitalOceanSpaces:
    @staticmethod
    async def upload_track(track_title_with_mp3: str) -> None:
        track_title_with_artists = track_title_with_mp3.replace(".mp3", "")
        with open(track_title_with_mp3, "rb") as downloaded_track:
            digital_ocean_spaces.upload_fileobj(
                Fileobj=downloaded_track,  # track which will be uploaded to Digital Ocean Spaces
                Bucket=settings.DO_SPACES_MUSIC_FOLDER_NAME,  # name of the directory in Digital Ocean Spaces
                Key=track_title_with_artists,  # name of the track
                ExtraArgs={"ACL": "public-read"},  # make the file public
            )

    async def check_if_track_exists_and_return_it(self, track_title_with_mp3: str) -> Union[str, None]:
        if await self.__check_if_track_exists(track_title_with_mp3=track_title_with_mp3):
            return await self.get_track(track_title_with_mp3=track_title_with_mp3)

        return None

    @staticmethod
    async def get_track(track_title_with_mp3: str) -> str:
        track_reference_on_digital_ocean_spaces = (
            f"{settings.DO_SPACES_ENDPOINT_URL}/{settings.DO_SPACES_MUSIC_FOLDER_NAME}/{track_title_with_mp3}"
        )
        return track_reference_on_digital_ocean_spaces

    @staticmethod
    async def __check_if_track_exists(track_title_with_mp3: str) -> bool:
        try:
            digital_ocean_spaces.get_object(
                Bucket=settings.DO_SPACES_MUSIC_FOLDER_NAME,
                Key=track_title_with_mp3,
            )  # check if the track exists in Digital Ocean Spaces
            return True
        except ClientError:
            return False
