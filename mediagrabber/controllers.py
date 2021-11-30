from common.controllers import Controller
from mediagrabber.universal_downloader import UniversalMediaDownloader


class MediaGrabberController(Controller):

    @property
    def title(self) -> str:
        return 'Скачивание аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    @property
    def menu_title(self) -> str:
        return 'Media Grabber'

    def main(self) -> bool:
        downloader = UniversalMediaDownloader()
        media_file = downloader.download()

        if media_file:
            media_file.move_to_downloads()
            print(media_file.info)
