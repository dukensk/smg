from dataclasses import dataclass


@dataclass
class OutputFormat:
    """Пресет выходного формата"""
    label: str = None
    preset: str = None
    postprocessors: list[dict[str, str]] = None
    type: str = None

    def __str__(self):
        return self.label

    @property
    def is_audio_only(self):
        return True if self.type == 'audio' else False



class OutputFormatMenu:
    _format_presets: list[OutputFormat]
    _default_output_format: OutputFormat

    def __init__(self, format_presets: list[OutputFormat]):
        self._format_presets = format_presets
        self._default_output_format = OutputFormat(label='Видео в максимальном качестве', preset='bestvideo+bestaudio/best')

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
        return 1 if not self.is_empty else 0

    @property
    def is_empty(self):
        """Проверяет, является ли меню пустым"""
        return True if not self._format_presets else False

    @property
    def default_output_format(self):
        """Выходной формат по умолчанию"""
        return self._default_output_format


output_formats = [
    OutputFormat(label='Аудио, m4a  (оптимально для YouTube)', preset='bestaudio[ext=m4a]/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}], type='audio'),
    OutputFormat(label='Видео, 1080p, mp4', preset='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 1440, mp4', preset='bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 4K, mp4', preset='bestvideo[height<=4096][ext=mp4]+bestaudio[ext=m4a]/best[height<=4096]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 1080p, webm', preset='bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 1440p, webm', preset='bestvideo[height<=1440]+bestaudio/best[height<=1440]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 4K, webm', preset='bestvideo[height<=4096]+bestaudio/best[height<=4096]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео в максимальном качестве', preset='bestvideo+bestaudio/best',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Аудио в максимальном качестве (оптимально для Twitch)', preset='bestaudio/best',
                 postprocessors=[
                     {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'},
                     {'key': 'FFmpegMetadata'}
                 ],
                 type='audio'),
]
