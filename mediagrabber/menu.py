from common.menu import FactoryMenu, MenuItem
from mediagrabber.downloaders import M4aAudioDownloader, BestQualityVideoDownloader, MediaDownloader

media_downloaders = {
    'audio_m4a': MenuItem('Аудио, m4a  (оптимально для YouTube)', M4aAudioDownloader),
    'video_best_quality': MenuItem('Видео в максимальном качестве)', BestQualityVideoDownloader),
}


class MediaDownloadersMenu(FactoryMenu):
    """Menu for choosing a media downloader"""

    @property
    def _input_message(self) -> str:
        return 'Выберите предпочтительный формат'

    def choose(self, item_key: str = None) -> MediaDownloader:
        return super(MediaDownloadersMenu, self).choose(item_key)
