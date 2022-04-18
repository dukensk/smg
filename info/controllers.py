from colorama import Style, Fore

from common.controllers import Controller
from common.notifications import show_push_notification
from info.downloaders import InfoDownloader


class InfoController(Controller):

    @property
    def header(self):
        return f'INFO ❯❯ {super(InfoController, self).header}'

    @property
    def title(self) -> str:
        return 'Получение информации о медиафайле'

    def main(self):
        downloader = InfoDownloader()
        self.show_app_header()
        print('\nПолучаем метаданные...')
        info = downloader.info
        self.show_app_header()
        print(f'\n{info}\n')
