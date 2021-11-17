import subprocess

from smg.filesystem import File


class MediaFile(File):

    @property
    def duration(self) -> float:
        """Duration in seconds"""
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", self.path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)


class AudioFile(MediaFile):
    EXTENSION_MP3 = '.mp3'
    EXTENSION_M4A = '.m4a'


class VideoFile(MediaFile):
    EXTENSION_MP4 = '.mp4'
    EXTENSION_MKV = '.mkv'
