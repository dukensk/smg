import os
from abc import ABC, abstractmethod
from time import sleep

import keyboard

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
        print('\nНажмите ENTER, чтобы продолжить или ESC, чтобы сменить режим работы')
        while True:
            key = keyboard.read_key(suppress=True)
            if key == 'enter':
                return False
            if key == 'esc':
                return True
