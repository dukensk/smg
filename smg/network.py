import urllib
from pathlib import Path
from urllib.error import ContentTooShortError
from colorama import Fore, Style
import validators
import wget

import settings
from smg.filesystem import File


def is_url(url: str) -> bool:
    """checks if the url is valid"""
    return False if not url or not validators.url(url) else True


class FileDownloader:
    """file downloader"""

    INPUT_URL_MESSAGE = 'URL скачиваемого файла'
    """message when requesting file url"""

    INPUT_URL_ERROR_MESSAGE = 'ЭТО НЕКОРРЕКТНЫЙ URL, ПОПРОБУЙТЕ ВВЕСТИ ДРУГОЙ'
    START_DOWNLOADING_MESSAGE = 'Скачиваем файл...'
    FINISH_DOWNLOADING_MESSAGE = 'ФАЙЛ УСПЕШНО СКАЧАН'
    ERROR_DOWNLOADING_MESSAGE = 'НЕ УДАЛОСЬ СКАЧАТЬ ФАЙЛ, ПРОБУЕМ СНОВА'

    _url: str

    def __init__(self, url: str = None):
        self._init_url(url)

    def _init_url(self, url: str | None = None):
        if not is_url(url):
            url = self._input_url()
        self._url = url

    def _input_url(self) -> str:
        url = None
        while not is_url(url):
            url = input('\n' + self.INPUT_URL_MESSAGE + ': ')
            if not is_url(url):
                print(Style.DIM + Fore.RED + self.INPUT_URL_ERROR_MESSAGE + Style.RESET_ALL)
        return url

    @property
    def _save_path(self) -> Path:
        return settings.SAVE_PATH

    def _show_start_downloading_message(self):
        print('\n' + self.START_DOWNLOADING_MESSAGE)

    def _show_finish_downloading_message(self):
        print(Style.DIM + Fore.GREEN + '\n' + self.FINISH_DOWNLOADING_MESSAGE + Style.RESET_ALL)

    def _show_error_downloading_message(self):
        print(Style.DIM + Fore.RED + '\n' + self.ERROR_DOWNLOADING_MESSAGE + Style.RESET_ALL)

    def download(self) -> File | None:
        """Downloads a file"""
        download_attempt = 0
        file_path = None
        while not file_path and download_attempt < settings.DOWNLOAD_ATTEMPTS_LIMIT:
            try:
                self._show_start_downloading_message()
                file_path = wget.download(self._url, out=str(self._save_path), bar=wget.bar_adaptive)
                self._show_finish_downloading_message()
            except urllib.error.ContentTooShortError:
                self._show_error_downloading_message()
                download_attempt += 1
                file_path = None

        return File(Path(file_path)) if file_path else None