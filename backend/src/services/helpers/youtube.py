from pytube import Search, YouTube
from pytube.exceptions import AgeRestrictedError


class YoutubeClient:
    @staticmethod
    def download_track(track_title_with_mp3: str) -> bool:
        youtube_track_link = Search(track_title_with_mp3).results[0].watch_url

        try:
            track = YouTube(youtube_track_link)
            stream = track.streams.filter(only_audio=True).first()
            stream.download(filename=track_title_with_mp3)  # download the track on the server
        except AgeRestrictedError:
            return True

        return False
