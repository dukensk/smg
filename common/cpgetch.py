import platform


class _Getch:
    """Gets a single character from standard input. Does not echo to the screen. Cross-platform solution.
    Using:
    inkey = _Getch()
        while True:
            sleep(0.1)
            key = inkey()
            if key == b'\r':
                return False
            if key == b'\x1b' or key == b'\x08':
                return True
    """

    def __init__(self):
        platform_name = platform.system()
        if platform_name == 'Windows':
            self.impl = _GetchWindows()
        else:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import getch
        return getch.getch()


windows_key_codes = {
    'enter': b'\r',
    'esc': b'\x1b',
    'backspace': b'\x08',
    'tab': b'\t',
    'space': b' ',
    '1': b'1',
    '2': b'2',
    '3': b'3',
    '4': b'4',
    '5': b'5',
    '6': b'6',
    '7': b'7',
    '8': b'8',
    '9': b'9',
    '0': b'0',
}

unix_key_codes = {
    'enter': '\n',
    'esc': '\x1b',
    'backspace': '\x7f',
    'tab': '\t',
    'space': ' ',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '0': '0',
}


def get_key_code(key: str) -> bytes | None:
    """Returns the code corresponding to the keys on the keyboard"""
    platform_name = platform.system()
    if platform_name == 'Windows':
        key_code = windows_key_codes.get(key)
    else:
        key_code = unix_key_codes.get(key)
    return key_code
