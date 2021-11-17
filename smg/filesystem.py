import os
from pathlib import Path


def get_system_downloads_path() -> Path:
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return Path(location)
    else:
        return Path.home() / 'Downloads'


class File:
    """Base file class"""
    _path: Path = None

    def __init__(self, path: Path):
        self._path = path

    @property
    def name(self) -> str:
        """Filename"""
        return self._path.stem

    @property
    def extension(self) -> str:
        """File extension with dot"""
        return self._path.suffix

    @property
    def path(self) -> Path:
        """Path to the file"""
        return self._path

    @property
    def name_with_extension(self) -> str:
        return self.name + self.extension

    def remove(self):
        """Removes file"""
        self.path.unlink(missing_ok=False)

    def _replace_path_and_remove_old_file(self, path: Path) -> bool:
        """Replaces the file path and removes the old file"""
        if path != self.path and path.exists():
            self.remove()
            self._path = path
            return True
        else:
            return False

    @property
    def size(self) -> int:
        """File size in bytes"""
        return self.path.stat().st_size
