from pytube import Search, YouTube


class YoutubeClient:
    @staticmethod
    def download_track(track_title_with_mp3: str) -> None:
        youtube_track_reference = Search(track_title_with_mp3).results[0].watch_url

        track = YouTube(youtube_track_reference)
        stream = track.streams.filter(only_audio=True).first()
        stream.download(filename=track_title_with_mp3)  # download the track on the server
