from abc import ABC, abstractmethod
import datetime as dt
from functools import lru_cache
from pathlib import Path
import yt_dlp
from colorama import Style, Fore

import settings
from common.downloaders import FileDownloader
from common.media import AudioFile, VideoFile
from common.service import is_youtube


class MetaDataLoader:
    """Media metadata loader"""
    _url: str

    def __init__(self, url: str = None):
        self._url = url

    @lru_cache(maxsize=1)
    def _get_metadata_by_url(self, url: str) -> dict[str, str]:
        ydl_opts = {
            'noplaylist': self._noplaylist,
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
    def duration(self) -> str:
        """Duration of the downloaded media file"""
        try:
            duration = str(dt.timedelta(seconds=float(self._metadata.get('duration'))))
        except TypeError:
            duration = 'ХЗ'
        return duration

    @property
    def upload_date(self) -> str:
        """Upload date of the downloaded media file"""
        try:
            upload_date = dt.datetime.strptime(self._metadata.get('upload_date'), '%Y%m%d').date().strftime('%d.%m.%Y')
        except TypeError:
            upload_date = 'ХЗ'
        return upload_date

    @property
    def uploader(self) -> str | None:
        """Author of the downloaded media file"""
        return self._metadata.get('uploader')

    @property
    def _noplaylist(self) -> bool:
        """Whether to ignore playlists, downloading only certain files"""
        return True


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
        return [{'key': 'FFmpegMetadata'}]

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
        download_attempt = 0
        file_path = None

        while not file_path and download_attempt < settings.MEDIAGRABBER_DOWNLOAD_ATTEMPTS_LIMIT:
            try:
                with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
                    yinfo = ydl.extract_info(self._url, download=True)
                file_path = ydl.prepare_filename(yinfo)
                print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
            except yt_dlp.DownloadError:
                download_attempt += 1
                file_path = None
                if download_attempt < settings.MEDIAGRABBER_DOWNLOAD_ATTEMPTS_LIMIT:
                    print(f'\n\n{Style.DIM}{Fore.LIGHTYELLOW_EX}ОЙ!{Style.RESET_ALL}')
                    print(f'Что-то пошло не так, '
                          f'пробуем возобновить загрузку [{download_attempt}/{settings.MEDIAGRABBER_DOWNLOAD_ATTEMPTS_LIMIT}]...')
                else:
                    print(f'\n\n{Style.DIM}{Fore.LIGHTRED_EX}YOU DIED{Style.RESET_ALL}')
                    print('\nНе удалось скачать видео. Нам очень жаль. :('
                          '\nТак бывает, если оно еще не до конца обработалось на сервисе или вы ввели неправильную ссылку. '
                          'Попробуйте позже.')

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

    title: str = 'Аудио, m4a'

    @property
    def _format(self) -> str:
        return 'bestaudio[ext=m4a]/best' if is_youtube(self.url) else 'bestaudio/best'

    @property
    def _postprocessors(self) -> list[dict[str, str]] | None:
        if is_youtube(self.url):
            postprocessors = [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'},
                {'key': 'FFmpegMetadata'}
            ]
        else:
            postprocessors = [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'}
            ]

        return postprocessors

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


class Mp4x720pVideoDownloader(MediaDownloader):
    """MP4 720p video downloader"""

    title: str = 'Видео, 720p, mp4'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'

    def download(self) -> VideoFile | None:
        return super(Mp4x720pVideoDownloader, self).download()


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


class BestQuality1080pVideoDownloader(MediaDownloader):
    """Best quality 1080p video downloader"""

    title: str = 'Видео, 1080p, наилучшее качество'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

    def download(self) -> VideoFile | None:
        return super(BestQuality1080pVideoDownloader, self).download()


class BestQuality1440pVideoDownloader(MediaDownloader):
    """Best quality 1440p video downloader"""

    title: str = 'Видео, 1440p, наилучшее качество'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'

    def download(self) -> VideoFile | None:
        return super(BestQuality1440pVideoDownloader, self).download()


class BestQuality4KVideoDownloader(MediaDownloader):
    """Best quality 4K video downloader"""

    title: str = 'Видео, 4K, наилучшее качество'

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=4096]+bestaudio/best[height<=4096]'

    def download(self) -> VideoFile | None:
        return super(BestQuality4KVideoDownloader, self).download()

class Mkv4KVideoDownloader(MediaDownloader):
    """MP4 4K video downloader"""

    title: str = 'Видео, 4K, mkv'

    @property
    def _ydl_opts(self):
        options = super()._ydl_opts
        options['merge_output_format'] = 'mkv'
        return options

    @property
    def _format(self) -> str:
        return 'bestvideo[height<=4096]+bestaudio/best'

    def download(self) -> VideoFile | None:
        return super(Mkv4KVideoDownloader, self).download()