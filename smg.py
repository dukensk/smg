import colorama

import settings
from common.service import init_working_directory
from smg.controllers import MainController
from smg.service import get_controller_key


def main():
    colorama.init(autoreset=True)
    init_working_directory(settings.TEMP_PATH)
    MainController().run(get_controller_key())


if __name__ == '__main__':
    main()
