from common.menu import MenuItem
from mediagrabber.downloaders import M4aAudioDownloader, Mp4x1080pVideoDownloader, Mp4x1440pVideoDownloader, Mp4x4KVideoDownloader, \
    Mp4x720pVideoDownloader, Mkv4KVideoDownloader

media_downloaders = {
    'audio_m4a': MenuItem(M4aAudioDownloader.title, M4aAudioDownloader),
    'video_mp4_1080p': MenuItem(Mp4x1080pVideoDownloader.title, Mp4x1080pVideoDownloader),
    'video_mp4_1440p': MenuItem(Mp4x1440pVideoDownloader.title, Mp4x1440pVideoDownloader),
    'video_mp4_4k': MenuItem(Mp4x4KVideoDownloader.title, Mp4x4KVideoDownloader),
    'video_mp4_720p': MenuItem(Mp4x720pVideoDownloader.title, Mp4x720pVideoDownloader),
    'video_mkv_4k': MenuItem(Mkv4KVideoDownloader.title, Mkv4KVideoDownloader),
}
