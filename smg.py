from smg.main import MainController
from smg.service import get_controller_key


def main():
    MainController().run(get_controller_key())


if __name__ == '__main__':
    main()
