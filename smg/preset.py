from dataclasses import dataclass


@dataclass
class OutputFormat:
    """Пресет выходного формата"""
    label: str = None
    preset: str = None
    postprocessors: [{str: str}] = None

    def __str__(self):
        return self.label


class OutputFormatMenu:
    _format_presets: [OutputFormat]

    def __init__(self, format_presets: [OutputFormat]):
        self._format_presets = format_presets

    def __str__(self):
        numbered_list = []
        for index, preset in enumerate(self._format_presets):
            numbered_list.append('{index}. {preset}'.format(index=index + 1, preset=str(preset)))
        return '\n'.join(numbered_list)

    def get_format_preset_by_index(self, format_index: int) -> OutputFormat | IndexError:
        if self.min_index <= format_index <= self.max_index and format_index > 0:
            return self._format_presets[format_index - 1]
        else:
            raise IndexError

    @property
    def max_index(self) -> int:
        """Возвращает максимальный допустимый номер пункта меню"""
        return len(self._format_presets)

    @property
    def min_index(self) -> 0:
        """Возвращает минимальный допустимый номер пункта меню"""
        if len(self._format_presets) > 0:
            min_format_index = 1
        else:
            min_format_index = 0
        return min_format_index


output_formats = [
    OutputFormat(label='Аудио, m4a  (оптимально для YouTube)', preset='bestaudio[ext=m4a]/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}]),
    OutputFormat(label='Видео, 1080p, mp4', preset='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'),
    OutputFormat(label='Видео, 1440, mp4', preset='bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]'),
    OutputFormat(label='Видео, 4K, mp4', preset='bestvideo[height<=4096][ext=mp4]+bestaudio[ext=m4a]/best[height<=4096]'),
    OutputFormat(label='Видео, 1080p, webm', preset='bestvideo[height<=1080]+bestaudio/best[height<=1080]'),
    OutputFormat(label='Видео, 1440p, webm', preset='bestvideo[height<=1440]+bestaudio/best[height<=1440]'),
    OutputFormat(label='Видео, 4K, webm', preset='bestvideo[height<=4096]+bestaudio/best[height<=4096]'),
    # OutputFormat(label='Видео, 720p', preset='bestvideo[height<=720]+bestaudio/best[height<=720]'),
    OutputFormat(label='Видео в максимальном качестве', preset='bestvideo+bestaudio/best'),
    OutputFormat(label='Аудио в максимальном качестве (оптимально для Twitch)', preset='bestaudio/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'}]),
]