from smg.filesystem import File


class AudioFile(File):
    EXTENSION_MP3 = '.mp3'
    EXTENSION_M4A = '.m4a'


class VideoFile(File):
    EXTENSION_MP4 = '.mp4'
    EXTENSION_MKV = '.mkv'
