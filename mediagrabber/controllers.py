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
        print('\nПолучаем метаданные...')
        info = downloader.info
        self.show_app_header()
        print(f'\n{info}\n')
        media_file = downloader.download()
        if media_file:
            media_file.move_to_downloads()
            print(f'\nИнформация о медиафайле: {media_file.info}')
            return True
        else:
            return False
