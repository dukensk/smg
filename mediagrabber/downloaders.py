from abc import ABC, abstractmethod
from pathlib import Path
import yt_dlp
from colorama import Style, Fore

import settings
from common.downloaders import FileDownloader
from common.media import AudioFile, VideoFile


class MediaDownloader(FileDownloader, ABC):
    """Abstract media downloader class"""
    INPUT_URL_MESSAGE = 'Введите URL видео'
    """message when requesting file url"""

    @property
    @abstractmethod
    def _format(self) -> str:
        """Download format"""

    @property
    def _save_path(self) -> Path:
        return settings.TEMP_PATH

    @property
    def _noplaylist(self) -> bool:
        """Whether to ignore playlists, downloading only certain files"""
        return True

    @property
    def _concurent_fragments(self) -> int:
        """The number of streams when downloading files, split into fragments"""
        return 3

    @property
    def _postprocessors(self) -> list[dict[str, str]] | None:
        """Postprocessors for converting uploaded media"""
        return None

    @property
    def _ydl_opts(self):
        ydl_opts = {
            'noplaylist': self._noplaylist,
            'format': self._format,
            'outtmpl': str(self._save_path) + '/%(title)s.%(ext)s',
            'concurrent-fragments': self._concurent_fragments,
        }
        if self._postprocessors:
            ydl_opts['postprocessors'] = self._postprocessors
        return ydl_opts

    def download(self) -> VideoFile | AudioFile | None:
        try:
            with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
                yinfo = ydl.extract_info(self._url, download=True)
            file_path = ydl.prepare_filename(yinfo)

            print(f'\n{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
            print('Все операции успешно завершены. Можно скачать что-нибудь еще.')
        except yt_dlp.DownloadError:
            print(f'\n\n{Style.DIM}{Fore.LIGHTRED_EX}YOU DIED{Style.RESET_ALL}')
            print('\nНе удалось скачать видео. Нам очень жаль. :('
                  '\nТак бывает, если оно еще не до конца обработалось на сервисе или вы ввели неправильную ссылку. '
                  'Попробуйте позже.')
            file_path = None

        return self._create_file(Path(file_path)) if file_path else None


class BestQualityVideoDownloader(MediaDownloader):
    """Best quality video downloader"""

    @property
    def _format(self) -> str:
        return 'bestvideo+bestaudio/best'

    def download(self) -> VideoFile | None:
        return super(BestQualityVideoDownloader, self).download()


class M4aAudioDownloader(MediaDownloader):
    """M4A audio downloader"""

    @property
    def _format(self) -> str:
        return 'bestaudio[ext=m4a]/best'

    def _postprocessors(self) -> list[dict[str, str]] | None:
        return [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}]

    def download(self) -> AudioFile | None:
        return super(M4aAudioDownloader, self).download()
