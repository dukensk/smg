import sys

from common.service import safe_list_get


def get_controller_key() -> str | None:
    """Gets the controller_key from parameters passed to the script at startup"""
    return safe_list_get(sys.argv, 1)


