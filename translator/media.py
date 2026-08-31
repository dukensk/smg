import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from colorama import Fore, Style

import settings
from common.media import AudioFile, VideoFile


class VoiceOver(AudioFile):
    _preprocessed: bool

    def __init__(self, path: Path, autopreprocess=True):
        super().__init__(path)
        self._preprocessed = False
        if autopreprocess:
            self.preprocess()

    @property
    def _preprocessed_filename(self) -> str:
        return self.name if self.is_preprocessed else f'{self.name}_preprocessed{self.EXTENSION_OPUS}'

    @property
    def _preprocessed_path(self) -> Path:
        return self.path if self.is_preprocessed else settings.TEMP_PATH / self._preprocessed_filename

    @property
    def is_preprocessed(self):
        return self._preprocessed

    def preprocess(self, target_sample_rate: int | str = 44100, codec: str = 'libvorbis'):
        if not self.is_preprocessed:
            print('\nПодготавливаем закадровый перевод...')
            subprocess.call(['ffmpeg',
                             '-i', self.path,
                             '-ar', str(target_sample_rate),
                             '-acodec', self._get_preprocessing_acodec(codec),
                             '-ac', '2',
                             '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_VIDEOFILE,
                             '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_BOOST),
                             self._preprocessed_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            self._replace_path_and_remove_old_file(self._preprocessed_path)
            self._preprocessed = True
            print(f'{Style.NORMAL}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        else:
            print('\nЗакадровый перевод уже подготовлен, дополнительная обработка не требуется')

    def _get_preprocessing_acodec(self, codec: str):
        acodecs = {
            'opus': 'libopus',
            'vorbis': 'libvorbis',
        }
        preprocessing_acodec = acodecs.get(codec)
        if not preprocessing_acodec:
            preprocessing_acodec = 'libvorbis'
        return preprocessing_acodec


class TranslatableMediaFile(ABC):
    """Media file to which you can add voiceover"""

    @abstractmethod
    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        """Adds voice-over translation"""


class TranslatableAudioFile(AudioFile, TranslatableMediaFile):
    """Audio file to which you can add voiceover fix"""

    _preprocessed: bool = False

    def __init__(self, path: Path, autopreprocess: bool = True):
        super().__init__(path)
        self._preprocessed = False
        if autopreprocess:
            self.preprocess()

    @property
    def is_preprocessed(self):
        return self._preprocessed

    @property
    def _preprocessed_filename(self) -> str:
        return f'{self.name}_preprocessed{self.EXTENSION_OPUS}'

    @property
    def _preprocessed_path(self) -> Path:
        return settings.TEMP_PATH / self._preprocessed_filename

    def preprocess(self):
        if not self.is_preprocessed:
            print('\nПодготавливаем аудио...')
            # Используем максимально полный набор флагов для копирования метаданных
            subprocess.call(['ffmpeg',
                             '-i', self.path,
                             '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_ORIGINAL_AUDIO),
                             '-map_metadata', '0',
                             self._preprocessed_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            self._preprocessed = True
            print(f'{Style.NORMAL}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')

        else:
            print('\nАудио уже по подготовлено к переводу, дополнительная обработка не требуется')


    def _format_time(self, seconds: float) -> str:
        """Преобразует секунды в формат HH:MM:SS."""
        total_seconds = int(round(seconds))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        return f'{hours:02}:{minutes:02}:{secs:02}'

    def _get_all_metadata(self) -> list[str]:
        """Извлекает все метаданные и формирует список глав для Description."""
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            '-show_chapters',  # Важно: извлекаем главы (Menu)
            str(self.path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        tags = {}

        # 1. Собираем все существующие теги в словарь
        if 'format' in data and 'tags' in data['format']:
            tags.update(data['format']['tags'])

        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'audio' and 'tags' in stream:
                # Добавляем теги потока, если их еще нет в словаре (приоритет формату)
                for k, v in stream['tags'].items():
                    if k not in tags:
                        tags[k] = v

        # 2. Обработка глав (Menu)
        chapters = data.get('chapters', [])
        if len(chapters) >= 3:
            chapter_lines = []
            for i, chap in enumerate(chapters):
                start_time_ms = float(chap['start'])
                start_time_sec = start_time_ms / 1000.0

                # Правило: Первая глава должна начинаться строго с 00:00:00
                if i == 0 and start_time_sec > 0:
                    time_str = '00:00:00'
                else:
                    time_str = self._format_time(start_time_sec)

                title = chap.get('tags', {}).get('title', 'Untitled')
                chapter_lines.append(f'{time_str} {title}')

            # Заменяем или добавляем Description списком глав
            tags['description'] = '\n'.join(chapter_lines)

        tags.pop('synopsis', None)
        tags.pop('comment', None)

        # 3. Преобразуем словарь в список аргументов для FFmpeg
        metadata_args = []
        for key, value in tags.items():
            metadata_args.extend(['-metadata', f'{key}={value}'])
        return metadata_args

    def add_voiceover(self, voiceover: VoiceOver) -> bool:
        print('\nНакладываем закадровый перевод...')
        output_file_path = self._output_file_path
        mixed_temp_path = output_file_path.with_suffix('.mixed.opus')
        # 1. Смешиваем звук
        subprocess.call(['ffmpeg',
                             '-i', self._preprocessed_path,
                             '-i', voiceover.path,
                             '-filter_complex', 'amix=inputs=2:duration=first',
                             '-b:a', str(settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_AUDIOFILE),
                             mixed_temp_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)

        # 2. Извлекаем все метаданные из оригинала (self.path)
        metadata_args = self._get_all_metadata()

        # 3. Создаем финальный файл: берем звук из микса и "впрыскиваем" метаданные
        subprocess.call(['ffmpeg',
                             '-i', mixed_temp_path,      # Input 0 (смешанный звук)
                             '-c', 'copy',               # Копируем поток без перекодирования
                             *metadata_args,              # Применяем все извлеченные теги
                             output_file_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)

        voiceover.remove()
        self.remove_preprocessed()
        self.remove()

        if mixed_temp_path.exists():
            mixed_temp_path.unlink()

        output_file_path.rename(self.path)
        print(f'{Style.NORMAL}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return True

    def remove_preprocessed(self):
        if self.is_preprocessed:
            self._preprocessed_path.unlink()
            self._preprocessed = False


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
                         '-acodec', self._get_acodec(self.audio_codec),
                         '-map_metadata', '1',
                         output_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT
                        )
        self.remove_preprocessed()
        self.remove()
        output_file_path.rename(self.path)
        print(f'{Style.NORMAL}{Fore.LIGHTGREEN_EX}ГОТОВО{Style.RESET_ALL}')
        return True

    def _get_acodec(self, codec: str):
        acodecs = {
            'opus': 'libopus',
            'aac': 'aac',
        }
        acodec = acodecs.get(codec)
        if not acodec:
            acodec = 'copy'
        return acodec


class TranslatableVideoFile(VideoFile, TranslatableMediaFile):
    """Video file to which you can add voiceover"""

    def extract_audio(self) -> TranslatableAudioTrackForVideoFile:
        return TranslatableAudioTrackForVideoFile(super().extract_audio().path)

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
        TranslatableAudioFile.EXTENSION_OPUS: TranslatableAudioFile,
        # video
        TranslatableVideoFile.EXTENSION_MP4: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_MKV: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_AVI: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_FLV: TranslatableVideoFile,
        TranslatableVideoFile.EXTENSION_WEBM: TranslatableVideoFile,
    }

    file_type = file_types.get(mediafile.extension)
    return file_type(mediafile.path) if file_type else None
