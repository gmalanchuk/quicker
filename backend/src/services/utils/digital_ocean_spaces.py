from src.config import digital_ocean_spaces, settings


class DigitalOceanSpaces:
    @staticmethod
    async def upload_track_and_link_back_to_it(track_title_with_mp3: str) -> str:
        with open(track_title_with_mp3, "rb") as downloaded_track:
            digital_ocean_spaces.upload_fileobj(
                Fileobj=downloaded_track,  # track which will be uploaded to Digital Ocean Spaces
                Bucket=settings.DO_SPACES_MUSIC_FOLDER_NAME,  # name of the directory in Digital Ocean Spaces
                Key=track_title_with_mp3,  # name of the track
                ExtraArgs={"ACL": "public-read"},  # make the file public
            )

        track_reference_on_digital_ocean_spaces = (
            f"{settings.DO_SPACES_ENDPOINT_URL}/{settings.DO_SPACES_MUSIC_FOLDER_NAME}/{track_title_with_mp3}"
        )
        return track_reference_on_digital_ocean_spaces
