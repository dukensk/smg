import subprocess
from pathlib import Path
from abc import ABC, abstractmethod

from colorama import Style, Fore

import settings
from common.media import AudioFile, VideoFile


class VoiceOver(AudioFile):
    _preprocessed: bool

    def __init__(self, path: Path, autopreprocess=True):
        super(VoiceOver, self).__init__(path)
        self._preprocessed = False
        if autopreprocess:
            self.preprocess()

    @property
    def _preprocessed_filename(self) -> str:
        return self.name if self.is_preprocessed else f'{self.name}_preprocessed{self.EXTENSION_OGG}'

    @property
    def _preprocessed_path(self) -> Path:
        return self.path if self.is_preprocessed else settings.TEMP_PATH / self._preprocessed_filename

    @property
    def is_preprocessed(self):
        return self._preprocessed

    def preprocess(self, target_sample_rate: int | str = 44100):
        if not self.is_preprocessed:
            print('\nПодготавливаем закадровый перевод...')
            subprocess.call(['ffmpeg',
                             '-i', self.path,
                             '-ar',  str(target_sample_rate),
                             '-acodec', 'libvorbis',
                             '-ac', '2',
                             '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_VIDEOFILE,
                             '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_BOOST),
                             self._preprocessed_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            self._replace_path_and_remove_old_file(self._preprocessed_path)
            self._preprocessed = True
            print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        else:
            print('\nЗакадровый перевод уже подготовлен, дополнительная обработка не требуется')


class TranslatableMediaFile(ABC):
    """Media file to which you can add voiceover"""

    @abstractmethod
    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        """Adds voice-over translation"""


class TranslatableAudioFile(AudioFile, TranslatableMediaFile):
    """Audio file to which you can add voiceover"""
    _preprocessed: bool

    def __init__(self, path: Path, autopreprocess: bool = True):
        super(TranslatableAudioFile, self).__init__(path)
        self._preprocessed = False
        if not autopreprocess:
            self.preprocess()

    @property
    def is_preprocessed(self):
        return self._preprocessed

    @property
    def _preprocessed_filename(self) -> str:
        return self.name if self.is_preprocessed else f'{self.name}_preprocessed{self.EXTENSION_M4A}'

    @property
    def _preprocessed_path(self) -> Path:
        return self.path if self.is_preprocessed else settings.TEMP_PATH / self._preprocessed_filename

    def preprocess(self):
        if not self.is_preprocessed:
            print('Подготавливаем аудио...')
            subprocess.call(['ffmpeg',
                             '-i', self.path,
                             '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_ORIGINAL_AUDIO),
                             self._preprocessed_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            self._replace_path_and_remove_old_file(self._preprocessed_path)
            self._preprocessed = True
            print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')

        else:
            print('\nАудио уже по подготовлено к переводу, дополнительная обработка не требуется')

    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        print('\nНакладываем закадровый перевод...')
        output_file_path = self._output_file_path
        subprocess.call(['ffmpeg',
                         '-i', voiceover.path,
                         '-i', self.path,
                         '-filter_complex', 'amix=inputs=2:duration=first',
                         '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_AUDIOFILE,
                         output_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT
                        )
        self.remove()
        output_file_path.rename(self.path)
        print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return True


class TranslatableAudioTrackForVideoFile(TranslatableAudioFile):
    """Audio track file for video to which you can add voiceover"""

    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        print('\nНакладываем закадровый перевод...')
        output_file_path = self._output_file_path
        subprocess.call(['ffmpeg',
                         '-i', voiceover.path,
                         '-i', self.path,
                         '-filter_complex', 'amix=inputs=2:duration=first',
                         '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_VIDEOFILE,
                         output_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT
                        )
        self.remove()
        output_file_path.rename(self.path)
        print(f'{Style.DIM}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return True


class TranslatableVideoFile(VideoFile, TranslatableMediaFile):
    """Video file to which you can add voiceover"""

    def extract_audio(self) -> TranslatableAudioTrackForVideoFile:
        return TranslatableAudioTrackForVideoFile(super(TranslatableVideoFile, self).extract_audio().path)

    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        audio = self.extract_audio()
        audio.add_voiceover(voiceover)
        self.replace_audio(audio)
        audio.remove()
        voiceover.remove()
        return True


def convert_to_translatable_mediafile(mediafile: VideoFile | AudioFile) -> TranslatableAudioFile | TranslatableVideoFile | None:
    """Converts a media object to translatable"""
    file_types = {
        # audio
        TranslatableAudioFile.EXTENSION_MP3: TranslatableAudioFile,
        TranslatableAudioFile.EXTENSION_AAC: TranslatableAudioFile,
        TranslatableAudioFile.EXTENSION_M4A: TranslatableAudioFile,
        TranslatableAudioFile.EXTENSION_OGG: TranslatableAudioFile,
        TranslatableAudioFile.EXTENSION_WAV: TranslatableAudioFile,
        # video
        TranslatableVideoFile.EXTENSION_MP4: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_MKV: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_AVI: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_FLV: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_WEBM: TranslatableVideoFile,
    }

    file_type = file_types.get(mediafile.extension)
    return file_type(mediafile.path) if file_type else None
