from pathlib import Path

import settings
from common.downloaders import FileDownloader


class DirectLinkDownloader(FileDownloader):

    @property
    def _save_path(self) -> Path:
        return settings.TEMP_PATH
