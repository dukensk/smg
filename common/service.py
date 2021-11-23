import os
from pathlib import Path

import validators


def safe_list_get(lst: list, index: int, default=None):
    """Safely retrieves an element of the list by index, if the element is absent, returns the default value"""
    try:
        return lst[index]
    except IndexError:
        return default


def is_url(url: str) -> bool:
    """checks if the url is valid"""
    return False if not url or not validators.url(url) else True


def init_working_directory(path: Path):
    """Initializing the application working directory"""
    os.chdir(path)
