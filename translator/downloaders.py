from pathlib import Path

import settings
from common.downloaders import FileDownloader
from mediagrabber.menu import MediaDownloadersMenu
from mediagrabber.universal_downloader import UniversalMediaDownloader
from translator.media import VoiceOver, TranslatableVideoFile, TranslatableAudioFile, convert_to_translatable_mediafile
from translator.menu import media_downloaders


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
        return VoiceOver(path, autopreprocess=False)

    def download(self) -> VoiceOver | None:
        return super().download()


class TranslatableMediaDownloader(UniversalMediaDownloader):

    def _init_downloader(self):
        self._downloader = MediaDownloadersMenu(media_downloaders, self._url).choose()

    def download(self) -> TranslatableAudioFile | TranslatableVideoFile | None:
        return convert_to_translatable_mediafile(super(TranslatableMediaDownloader, self).download())
