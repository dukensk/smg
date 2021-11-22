import sys

import validators


def safe_list_get(lst: list, index: int, default=None):
    """Safely retrieves an element of the list by index, if the element is absent, returns the default value"""
    try:
        return lst[index]
    except IndexError:
        return default


def get_controller_key() -> str | None:
    """Gets the controller_key from parameters passed to the script at startup"""
    return safe_list_get(sys.argv, 1)


def is_url(url: str) -> bool:
    """checks if the url is valid"""
    return False if not url or not validators.url(url) else True
