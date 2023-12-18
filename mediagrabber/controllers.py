from colorama import Style, Fore

from common.controllers import Controller
from common.notifications import show_push_notification
from mediagrabber.universal_downloader import UniversalMediaDownloader


class MediaGrabberController(Controller):

    @property
    def header(self):
        return f'{Fore.LIGHTGREEN_EX}MEDIAGRABBER ❯❯{Style.RESET_ALL} {super(MediaGrabberController, self).header}'

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
        media_file = downloader.download()
        if media_file:
            media_file.move_to_downloads()
            self.show_app_header()
            print(f'\n{info}')
            print(f'\n{Style.NORMAL}{Fore.LIGHTGREEN_EX}ВСЕ ОПЕРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ{Style.RESET_ALL}')
            print(f'Скачан медиафайл: {media_file.info}')
            show_push_notification('Скачан медиафайл',
                                   f'{media_file.name_with_extension} [{media_file.formatted_size}]',
                                   'mediagrabber_icon.ico', 'SMG: MEDIAGRABBER')
            return True
        else:
            show_push_notification('Не удалось скачать медиафайл',
                                   f'{downloader.metadata.title}', 'mediagrabber_icon.ico', 'SMG: MEDIAGRABBER')
            return False
