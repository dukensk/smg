import colorama

from smg.controllers import MainController
from smg.service import get_controller_key


def main():
    colorama.init(autoreset=True)
    MainController().run(get_controller_key())


if __name__ == '__main__':
    main()
