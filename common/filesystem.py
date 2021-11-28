import os
from pathlib import Path

import settings


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

    @property
    def size_in_kb(self) -> float:
        return self.size / 1024

    @property
    def size_in_mb(self) -> float:
        return self.size / (1024 * 1024)

    @property
    def size_in_gb(self) -> float:
        return self.size / (1024 * 1024 * 1024)

    @property
    def formatted_size(self) -> str:
        if self.size < 1024:
            size = f'{self.size} Б'
        elif 1024 <= self.size < 1024 * 1024:
            size = f'{"%.2f" % self.size_in_kb} Кб'
        elif 1024 * 1024 <= self.size < 1024 * 1024 * 1024:
            size = f'{"%.2f" % self.size_in_mb} Мб'
        elif self.size >= 1024 * 1024 * 1024:
            size = f'{"%.2f" % self.size_in_gb} Гб'
        else:
            size = f'{self.size} Б'
        return size

    def _get_unique_new_path(self, path: Path) -> path:
        """Returns a unique path to move the file, if a file with the same name already exists, a counter is added to the name"""
        unique_path = path / self.name_with_extension
        counter = 0
        while True:
            if not unique_path.exists():
                return unique_path
            else:
                counter += 1
                unique_path = path / f'{self.name} ({counter}){self.extension}'

    def move_to(self, path: Path) -> Path:
        """
        Moves the file
        :param path: path to destination directory
        :return:
        """
        new_path = self._get_unique_new_path(path)
        if self._path.rename(new_path):
            self._path = new_path
        return self.path

    def move_to_downloads(self) -> Path:
        """Moves the file to the downloads directory"""
        self.move_to(settings.SAVE_PATH)
        return self.path

    @property
    def info(self) -> str:
        """File information"""
        return f'{self.name_with_extension} | {self.formatted_size}'
