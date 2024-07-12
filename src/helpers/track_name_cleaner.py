class TrackNameCleaner:
    @staticmethod
    async def get_cleaned_track_name(track_name: str, track_artists: str) -> str:
        # replace '/' with '_' in the track name because '/' is not allowed in a file name and is treated as a directory
        if "/" in track_name:
            track_name = track_name.replace("/", "_")

        full_track_name_with_mp3 = f"{track_artists} - {track_name}.mp3"

        return full_track_name_with_mp3
