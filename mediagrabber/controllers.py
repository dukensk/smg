from colorama import Fore, Style

from common.chapters_service import chapters_postprocess
from common.controllers import Controller
from common.notifications import show_push_notification
from mediagrabber.universal_downloader import UniversalMediaDownloader


class MediaGrabberController(Controller):
    @property
    def header(self):
        return f'{Fore.LIGHTGREEN_EX}MEDIAGRABBER ❯❯{Style.RESET_ALL} {super().header}'

    @property
    def title(self) -> str:
        return 'Скачивание аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    def main(self) -> bool:
        downloader = UniversalMediaDownloader()
        self.show_app_header()
        print('\nПолучаем метаданные...')
        info = downloader.info
        self.show_app_header()
        print(f'\n{info}\n')
        mediafile = downloader.download()
        if mediafile:
            mediafile = chapters_postprocess(mediafile)

            mediafile.move_to_downloads()
            self.show_app_header()
            print(f'\n{info}')
            print(f'\n{Style.NORMAL}{Fore.LIGHTGREEN_EX}ВСЕ ОПЕРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ{Style.RESET_ALL}')
            print(f'Скачан медиафайл: {mediafile.info}')
            show_push_notification(
                'Скачан медиафайл',
                f'{mediafile.name_with_extension} [{mediafile.formatted_size}]',
                'mediagrabber_icon.ico',
                'SMG: MEDIAGRABBER',
            )
            return True
        else:
            show_push_notification(
                'Не удалось скачать медиафайл', f'{downloader.metadata.title}', 'mediagrabber_icon.ico', 'SMG: MEDIAGRABBER'
            )
            return False
