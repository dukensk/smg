from abc import ABC, abstractmethod
import datetime as dt
from functools import lru_cache
from pathlib import Path
import yt_dlp
from colorama import Style, Fore

import settings
from common.downloaders import FileDownloader
from common.media import AudioFile, VideoFile


class MetaDataLoader:
    """Media metadata loader"""
    _url: str

    def __init__(self, url: str = None):
        self._url = url

    @lru_cache(maxsize=1)
    def _get_metadata_by_url(self, url: str) -> dict[str, str]:
        ydl_opts = {
            'quiet': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                metadata = ydl.extract_info(url, download=False)
        except yt_dlp.DownloadError:
            metadata = {}
        return metadata

    @property
    def _metadata(self) -> dict[str, str]:
        return self._get_metadata_by_url(self._url)

    @property
    def title(self) -> str | None:
        """Title of the downloaded media file"""
        return self._metadata.get('title')

    @property
    def format(self) -> str | None:
        """Format of the downloaded media file"""
        return self._metadata.get('format')

    @property
    def duration(self) -> str | None:
        """Duration of the downloaded media file"""
        return str(dt.timedelta(seconds=float(self._metadata.get('duration'))))

    @property
    def upload_date(self) -> str | None:
        """Upload date of the downloaded media file"""
        return dt.datetime.strptime(self._metadata.get('upload_date'), '%Y%m%d').date().strftime('%d.%m.%Y')

    @property
    def uploader(self) -> str | None:
        """Author of the downloaded media file"""
        return self._metadata.get('uploader')


class MediaDownloader(FileDownloader, ABC):
    """Abstract media downloader class"""

    title: str = 'Загрузчик медиафайлов'

    INPUT_URL_MESSAGE = 'Введите URL видео'
    """message when requesting file url"""

    _metadata: MetaDataLoader

    def __init__(self, url: str = None):
        super(MediaDownloader, self).__init__(url)
        self._init_metadata()

    def _init_metadata(self):
        if self._url:
            self._metadata = MetaDataLoader(self._url)

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

    @property
    def metadata(self) -> MetaDataLoader:
        return self._metadata

    @property
    def info(self) -> str:
        info = f'Видео: {self.metadata.title}' \
               f'\nФормат: {self.metadata.format}' \
               f'\nПродолжительность: {self.metadata.duration} | Опубликовано: {self.metadata.upload_date}' \
               f'\nАвтор: {self.metadata.uploader}' \
               f'\n\nВыбран профиль загрузки: {self.title}'
        return info

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

    title: str = 'Видео в максимальном качестве'

    @property
    def _format(self) -> str:
        return 'bestvideo+bestaudio/best'

    def download(self) -> VideoFile | None:
        return super(BestQualityVideoDownloader, self).download()


class M4aAudioDownloader(MediaDownloader):
    """M4A audio downloader"""

    title: str = 'Аудио, m4a (оптимально для YouTube)'

    @property
    def _format(self) -> str:
        return 'bestaudio[ext=m4a]/best'

    @property
    def _postprocessors(self) -> list[dict[str, str]] | None:
        return [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}]

    def download(self) -> AudioFile | None:
        return super(M4aAudioDownloader, self).download()


class Mp4x1080pVideoDownloader(MediaDownloader):
    """MP4 1080p video downloader"""

    title: str = 'Видео, 1080p, mp4'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'

    def download(self) -> VideoFile | None:
        return super(Mp4x1080pVideoDownloader, self).download()


class Mp4x1440pVideoDownloader(MediaDownloader):
    """MP4 1440p video downloader"""

    title: str = 'Видео, 1440p, mp4'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]'

    def download(self) -> VideoFile | None:
        return super(Mp4x1440pVideoDownloader, self).download()


class Mp4x4KVideoDownloader(MediaDownloader):
    """MP4 4K video downloader"""

    title: str = 'Видео, 4K, mp4'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=4096][ext=mp4]+bestaudio[ext=m4a]/best[height<=4096]'

    def download(self) -> VideoFile | None:
        return super(Mp4x4KVideoDownloader, self).download()


class Webm1080pVideoDownloader(MediaDownloader):
    """WEBM 1080p video downloader"""

    title: str = 'Видео, 1080p, webm'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

    def download(self) -> VideoFile | None:
        return super(Webm1080pVideoDownloader, self).download()


class Webm1440pVideoDownloader(MediaDownloader):
    """WEBM 1440p video downloader"""

    title: str = 'Видео, 1440p, webm'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'

    def download(self) -> VideoFile | None:
        return super(Webm1440pVideoDownloader, self).download()
