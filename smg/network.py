import validators


def is_url(url: str) -> bool:
    """checks if the url is valid"""
    return False if not url or not validators.url(url) else True


