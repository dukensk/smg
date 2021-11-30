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
        self.show_app_header()
        # TODO Добавить вывод информации о скачиваемом видео
        media_file = downloader.download()
        if media_file:
            media_file.move_to_downloads()
            print('\nИнформация о медиафайле: {media_file.info}')
            return True
