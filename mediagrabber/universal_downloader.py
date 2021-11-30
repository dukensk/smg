from pathlib import Path

import settings
from common.downloaders import FileDownloader
from common.media import AudioFile, VideoFile
from mediagrabber.downloaders import MediaDownloader
from mediagrabber.menu import MediaDownloadersMenu, media_downloaders


class UniversalMediaDownloader(FileDownloader):
    INPUT_URL_MESSAGE = 'Введите URL видео'
    """message when requesting file url"""

    _downloader: MediaDownloader

    def __init__(self, url: str = None):
        super(UniversalMediaDownloader, self).__init__(url)
        self._init_downloader()

    def _init_downloader(self):
        self._downloader = MediaDownloadersMenu(media_downloaders, self._url).choose()

    @property
    def _save_path(self) -> Path:
        return settings.TEMP_PATH

    @property
    def info(self) -> str:
        return self._downloader.info

    def download(self) -> AudioFile | VideoFile | None:
        return self._downloader.download()
