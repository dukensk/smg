import os
from pathlib import Path
from urllib.parse import urlparse

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


def is_youtube(url: str) -> bool:
    """Checks if the domain belongs to YouTube"""
    if not is_url(url):
        return False

    youtube_domains = (
        'www.youtube.com',
        'youtube.com',
        'www.youtu.be',
        'youtu.be',
        'youtube.com.br',
        'youtube.co.nz',
        'youtube.de',
        'youtube.es',
        'youtube.it',
        'youtube.nl',
        'youtube-nocookie.com',
        'youtube.ru',
    )

    domain = urlparse(url).netloc
    return domain in youtube_domains
