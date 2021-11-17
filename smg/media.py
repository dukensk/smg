from json import loads
import datetime
from pathlib import Path
from subprocess import check_output

from smg.filesystem import File


class MediaFile(File):
    _media_info: dict

    def __init__(self, path: Path):
        super(MediaFile, self).__init__(path)
        self._media_info = {}

    def _clear_media_info(self):
        self._media_info.clear()

    def remove(self):
        super(MediaFile, self).remove()
        self._clear_media_info()

    @property
    def media_info(self) -> dict:
        if not self._media_info:
            result = check_output(['ffprobe',
                                   '-hide_banner', '-loglevel', 'panic',
                                   '-show_format',
                                   '-show_streams',
                                   '-of',
                                   'json', self.path])
            self._media_info = loads(result)
        return self._media_info

    @property
    def duration(self) -> str:
        """Duration"""
        return str(datetime.timedelta(seconds=self.duration_in_seconds))

    @property
    def duration_in_seconds(self):
        """Duration in seconds"""
        return float(self.media_info.get('format').get('duration'))



class AudioFile(MediaFile):
    EXTENSION_MP3 = '.mp3'
    EXTENSION_M4A = '.m4a'

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
        return f'{self.name_with_extension} | {self.duration[:-3]} | {self.bitrate} kbps | {self.samplerate} Hz | ' \
               f'{self.codec_name} | каналов: {self.channels} | {self.formatted_size}'


class VideoFile(MediaFile):
    EXTENSION_MP4 = '.mp4'
    EXTENSION_MKV = '.mkv'
