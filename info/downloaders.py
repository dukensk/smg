from mediagrabber.downloaders import MediaDownloader


class InfoDownloader(MediaDownloader):
    """InfoDownloader class"""

    @property
    def _format(self) -> str | None:
        return None

    @property
    def info(self) -> str:
        info = f'Видео: {self.metadata.title}' \
               f'\nФормат: {self.metadata.format}' \
               f'\nПродолжительность: {self.metadata.duration} | Опубликовано: {self.metadata.upload_date}' \
               f'\nАвтор: {self.metadata.uploader}'
        return info
