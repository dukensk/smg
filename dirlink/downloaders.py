from pathlib import Path

import settings
from common.downloaders import FileDownloader
from common.filesystem import File


class DirectLinkDownloader(FileDownloader):

    @property
    def _save_path(self) -> Path:
        return settings.TEMP_PATH

    def _create_file(self, path: Path) -> File:
        return File(path)
