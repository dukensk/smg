import os
from abc import ABC, abstractmethod
from time import sleep

from common.cpgetch import _Getch, get_key_code
from smg.version import app_version


class Controller(ABC):
    """Base abstract controller class"""

    def run(self) -> bool:
        """Run the controller"""
        is_escaped = False
        while not is_escaped:
            self.show_app_header()
            self.main()
            is_escaped = self._is_escaped
        return True

    @abstractmethod
    def main(self):
        """The main controller method in which the main work should take place"""

    def show_app_header(self):
        """Shows the title of the application"""
        self.clear_console()
        print(f'{self.header}\n{self.title}')

    @staticmethod
    def clear_console():
        """Clears the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @property
    def header(self):
        """The main title of the application"""
        return f'Simple Media Grabber by Duke {app_version}'

    @property
    @abstractmethod
    def title(self) -> str:
        """Controller title"""

    @property
    @abstractmethod
    def menu_title(self) -> str:
        """Controller title in the menu"""

    @property
    def _is_escaped(self) -> bool:
        """Asks the user whether to change the application mode"""
        sleep(0.2)
        print('\nНажмите одну из клавиш:'
              '\n[ENTER] – продолжить в том же режиме'
              '\n[ESC] или [Backspace] – сменить режим работы приложения')
        inkey = _Getch()
        while True:
            sleep(0.1)
            key = inkey()
            if key == get_key_code('enter'):
                return False
            if key == get_key_code('esc') or key == get_key_code('backspace'):
                return True
