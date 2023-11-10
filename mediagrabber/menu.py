from typing import Type

from common.menu import FactoryMenu, MenuItem
from mediagrabber.downloaders import BestQualityVideoDownloader, MediaDownloader, M4aAudioDownloader, Mp4x1080pVideoDownloader, \
    Mp4x1440pVideoDownloader, Mp4x4KVideoDownloader, BestQuality1080pVideoDownloader, BestQuality1440pVideoDownloader, \
    BestQuality4KVideoDownloader, Mp4x720pVideoDownloader, Mkv4KVideoDownloader

media_downloaders = {
    'audio_m4a': MenuItem(M4aAudioDownloader.title, M4aAudioDownloader),
    'video_mp4_1080p': MenuItem(Mp4x1080pVideoDownloader.title, Mp4x1080pVideoDownloader),
    'video_mkv_4k': MenuItem(Mkv4KVideoDownloader.title, Mkv4KVideoDownloader),
    'video_mp4_1440p': MenuItem(Mp4x1440pVideoDownloader.title, Mp4x1440pVideoDownloader),
    'video_mp4_4k': MenuItem(Mp4x4KVideoDownloader.title, Mp4x4KVideoDownloader),
    'video_best_quality_1080p': MenuItem(BestQuality1080pVideoDownloader.title, BestQuality1080pVideoDownloader),
    'video_best_quality_1440p': MenuItem(BestQuality1440pVideoDownloader.title, BestQuality1440pVideoDownloader),
    # 'video_best_quality_4k': MenuItem(BestQuality4KVideoDownloader.title, BestQuality4KVideoDownloader),
    'video_best_quality': MenuItem(BestQualityVideoDownloader.title, BestQualityVideoDownloader),
    'video_mp4_720p': MenuItem(Mp4x720pVideoDownloader.title, Mp4x720pVideoDownloader),
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
