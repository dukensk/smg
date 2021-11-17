import subprocess
from json import loads
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
    def duration(self) -> float:
        """Duration in seconds"""
        return float(self.media_info.get('format').get('duration'))

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


class AudioFile(MediaFile):
    EXTENSION_MP3 = '.mp3'
    EXTENSION_M4A = '.m4a'


class VideoFile(MediaFile):
    EXTENSION_MP4 = '.mp4'
    EXTENSION_MKV = '.mkv'
