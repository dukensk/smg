import subprocess
from pathlib import Path

from colorama import Style, Fore

import settings
from common.media import AudioFile


class VoiceOver(AudioFile):
    _preprocessed: bool

    def __init__(self, path: Path, autopreprocess=True):
        super(VoiceOver, self).__init__(path)
        self._preprocessed = False
        if autopreprocess:
            self.preprocess()

    @property
    def _preprocessed_filename(self) -> str:
        return self.name if self.is_preprocessed else f'{self.name}_preprocessed{self.EXTENSION_M4A}'

    @property
    def _preprocessed_path(self) -> Path:
        return self.path if self.is_preprocessed else settings.TEMP_PATH / self._preprocessed_filename

    @property
    def is_preprocessed(self):
        return self._preprocessed

    def preprocess(self):
        if not self.is_preprocessed:
            print('\nПодготавливаем закадровый перевод...')
            subprocess.call(['ffmpeg',
                             '-i', self.path,
                             '-ar', '44100',
                             '-ac', '2',
                             '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE,
                             '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_BOOST),
                             self._preprocessed_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            self._replace_path_and_remove_old_file(self._preprocessed_path)
            print(Style.DIM + Fore.GREEN + 'ГОТОВО' + Style.RESET_ALL)
        else:
            print('\nЗакадровый перевод уже подготовлен, дополнительная обработка не требуется')