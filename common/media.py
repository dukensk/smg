import datetime
from functools import lru_cache
from json import loads
from pathlib import Path
import subprocess
from subprocess import check_output

from colorama import Style, Fore

import settings
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

    @property
    def _output_file_path(self) -> Path:
        return self.path.parent.absolute() / self._output_file_name

    @property
    def _output_file_name(self) -> str:
        return f'{self.name}_output{self.extension}'


class AudioFile(MediaFile):
    EXTENSION_M4A = '.m4a'
    EXTENSION_MP3 = '.mp3'
    EXTENSION_AAC = '.aac'
    EXTENSION_OGG = '.ogg'
    EXTENSION_WAV = '.wav'

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
            return f'{self.name_with_extension}' \
                   f'\n{self.formatted_size} | {self.duration[:-3]} | аудио | ' \
                   f'{self.codec_name} | {self.bitrate} kbps | {self.samplerate} Hz | каналов: {self.channels}'
        except FileNotFoundError:
            return f'\n{Style.DIM}{Fore.LIGHTRED_EX}ОШИБКА:{Style.RESET_ALL} Файла {self.path} не существует'


class VideoFile(MediaFile):
    EXTENSION_MP4 = '.mp4'
    EXTENSION_MKV = '.mkv'
    EXTENSION_AVI = '.avi'
    EXTENSION_FLV = '.flv'
    EXTENSION_WEBM = '.webm'

    @property
    def info(self) -> str:
        return f'{self.name_with_extension}' \
               f'\n{self.formatted_size} | {self.duration[:-3]} | видео | {self.resolution} {self.framerate} FPS'

    @property
    def width(self) -> int:
        """video width"""
        return int(self.media_info.get('streams')[0].get('width'))

    @property
    def height(self) -> int:
        """video height"""
        return int(self.media_info.get('streams')[0].get('height'))

    @property
    def resolution(self) -> str:
        """video resolution"""
        return f'{self.width}x{self.height}'

    @property
    def framerate(self) -> str:
        """video framerate"""
        return self.media_info.get('streams')[0].get('r_frame_rate')[:-2]

    @property
    def _extracted_audio_filename(self) -> str:
        return f'{self.name}{AudioFile.EXTENSION_M4A}'

    @property
    def _extracted_audio_path(self) -> Path:
        return settings.TEMP_PATH / self._extracted_audio_filename

    def extract_audio(self) -> AudioFile:
        """Extract audio"""
        print('\nИзвлекаем аудио...')
        subprocess.call(['ffmpeg',
                         '-i', self.path,
                         '-vn',
                         '-acodec', 'copy',
                         self._extracted_audio_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return AudioFile(self._extracted_audio_path)

    def replace_audio(self, audiofile: AudioFile) -> bool:
        """Replaces the audio track in the video"""
        print('\nЗаменяем аудио...')
        output_file_path = self._output_file_path
        subprocess.call(['ffmpeg',
                         '-i', self.path,
                         '-i', audiofile.path,
                         '-c', 'copy',
                         '-map', '0:v:0',
                         '-map', '1:a:0',
                         output_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT
                        )
        self.remove()
        output_file_path.rename(self.path)
        print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return True


class ImageFile(File):
    EXTENSION_JPG = '.jpg'
    EXTENSION_JPEG = '.jpeg'
    EXTENSION_PNG = '.png'
    EXTENSION_GIF = '.gif'
    EXTENSION_BMP = '.bmp'

    @property
    def info(self) -> str:
        return f'{self.name_with_extension} | {self.formatted_size} | изображение'


def create_file_object(path: Path) -> File | AudioFile | VideoFile | ImageFile:
    """Factory function to create a file object according to the extension of the physical file"""
    file_types = {
        # audio
        AudioFile.EXTENSION_MP3: AudioFile,
        AudioFile.EXTENSION_AAC: AudioFile,
        AudioFile.EXTENSION_M4A: AudioFile,
        AudioFile.EXTENSION_OGG: AudioFile,
        AudioFile.EXTENSION_WAV: AudioFile,
        # video
        VideoFile.EXTENSION_MP4: VideoFile,
        VideoFile.EXTENSION_MKV: VideoFile,
        VideoFile.EXTENSION_AVI: VideoFile,
        VideoFile.EXTENSION_FLV: VideoFile,
        VideoFile.EXTENSION_WEBM: VideoFile,
        # images
        ImageFile.EXTENSION_JPG: ImageFile,
        ImageFile.EXTENSION_JPEG: ImageFile,
        ImageFile.EXTENSION_PNG: ImageFile,
        ImageFile.EXTENSION_GIF: ImageFile,
        ImageFile.EXTENSION_BMP: ImageFile,
    }

    file_type = file_types.get(path.suffix)
    if not file_type:
        file_type = File

    return file_type(path)
