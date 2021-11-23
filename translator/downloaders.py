from pathlib import Path

import settings
from common.downloaders import FileDownloader
from translator.media import VoiceOver


class VoiceOverDownloader(FileDownloader):
    INPUT_URL_MESSAGE = 'Введите URL закадрового перевода'
    """message when requesting voiceover url"""

    START_DOWNLOADING_MESSAGE = 'Скачиваем закадровый перевод...'
    FINISH_DOWNLOADING_MESSAGE = 'ЗАКАДРОВЫЙ ПЕРЕВОД УСПЕШНО СКАЧАН'
    ERROR_DOWNLOADING_MESSAGE = 'НЕ УДАЛОСЬ СКАЧАТЬ ЗАКАДРОВЫЙ ПЕРЕВОД, ПРОБУЕМ СНОВА'

    @property
    def _save_path(self) -> Path:
        return settings.TEMP_PATH

    def _create_file(self, path: Path) -> VoiceOver:
        return VoiceOver(path)

    def download(self) -> VoiceOver | None:
        return super().download()