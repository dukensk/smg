import datetime
from functools import lru_cache
from json import loads
from pathlib import Path
from subprocess import check_output

from colorama import Style, Fore

from common.filesystem import File


class MediaFile(File):

    def __init__(self, path: Path):
        super(MediaFile, self).__init__(path)

    @property
    def media_info(self) -> dict:
        return self._get_media_info_by_path(self.path)

    @lru_cache(maxsize=1)
    def _get_media_info_by_path(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError

        result = check_output(['ffprobe',
                               '-hide_banner', '-loglevel', 'panic',
                               '-show_format',
                               '-show_streams',
                               '-of',
                               'json', path])

        return loads(result)

    @property
    def duration(self) -> str:
        """Duration"""
        return str(datetime.timedelta(seconds=self.duration_in_seconds))

    @property
    def duration_in_seconds(self):
        """Duration in seconds"""
        return float(self.media_info.get('format').get('duration'))


class AudioFile(MediaFile):

    @property
    def bitrate(self) -> int:
        """bitrate, kbps"""
        return int(int(self.media_info.get('format').get('bit_rate')) / 1000)

    @property
    def samplerate(self) -> int:
        """Sampling frequency, Hz"""
        return int(self.media_info.get('streams')[0].get('sample_rate'))

    @property
    def codec_name(self) -> str:
        """Codec name"""
        return str(self.media_info.get('streams')[0].get('codec_name'))

    @property
    def channels(self) -> int:
        """Count of channels"""
        return int(self.media_info.get('streams')[0].get('channels'))

    def __str__(self):
        return f'{self.name_with_extension}'

    @property
    def info(self) -> str:
        try:
            return f'{self.name_with_extension} | {self.formatted_size} | {self.duration[:-3]} | аудио | ' \
                   f'{self.codec_name} | {self.bitrate} kbps | {self.samplerate} Hz | каналов: {self.channels}'
        except FileNotFoundError:
            return f'\n{Style.DIM}{Fore.LIGHTRED_EX}ОШИБКА:{Style.RESET_ALL} Файла {self.path} не существует'


class VideoFile(MediaFile):
    @property
    def info(self) -> str:
        return f'{self.name_with_extension} | {self.formatted_size} | видео'


class ImageFile(File):
    @property
    def info(self) -> str:
        return f'{self.name_with_extension} | {self.formatted_size} | изображение'


def create_file_object(path: Path) -> File | AudioFile | VideoFile | ImageFile:
    """Factory function to create a file object according to the extension of the physical file"""
    file_types = {
        # audio
        '.mp3': AudioFile,
        '.aac': AudioFile,
        '.m4a': AudioFile,
        '.ogg': AudioFile,
        # video
        '.mp4': VideoFile,
        '.mkv': VideoFile,
        '.avi': VideoFile,
        '.flv': VideoFile,
        '.webm': VideoFile,
        # images
        '.jpg': ImageFile,
        '.jpeg': ImageFile,
        '.png': ImageFile,
        '.bmp': ImageFile,
    }

    file_type = file_types.get(path.suffix)
    if not file_type:
        file_type = File

    return file_type(path)
