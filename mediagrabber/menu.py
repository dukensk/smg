from typing import Type

from common.menu import FactoryMenu, MenuItem
from mediagrabber.downloaders import BestQualityVideoDownloader, MediaDownloader, M4aAudioDownloader, Mp4x1080pVideoDownloader, \
    Mp4x1440pVideoDownloader

media_downloaders = {
    'audio_m4a': MenuItem(M4aAudioDownloader.title, M4aAudioDownloader),
    'video_best_quality': MenuItem(BestQualityVideoDownloader.title, BestQualityVideoDownloader),
    'video_mp4_1080p': MenuItem(Mp4x1080pVideoDownloader.title, Mp4x1080pVideoDownloader),
    'video_mp4_1440p': MenuItem(Mp4x1440pVideoDownloader.title, Mp4x1440pVideoDownloader),
}


class MediaDownloadersMenu(FactoryMenu):
    """Menu for choosing a media downloader"""

    _url: str = None

    def __init__(self, items: dict[str, MenuItem] = None, url: str = None):
        super(MediaDownloadersMenu, self).__init__(items)
        self._url = url

    @property
    def _input_message(self) -> str:
        return 'Выберите предпочтительный формат'

    def choose(self, item_key: str = None) -> MediaDownloader:
        return super(MediaDownloadersMenu, self).choose(item_key)

    def _create_instance(self, object_type: Type):
        """
        Creates an instance of an object
        :param object_type: тип создаваемого объекта
        :return:
        """
        return object_type(self._url)
