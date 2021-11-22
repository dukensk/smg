from colorama import Style, Fore

from common.controllers import Controller
from mediagrabber.controllers import MediaGrabberController
from translator.controllers import TranslatorController

controllers = {
    'mediagrabber': MediaGrabberController(),
    'translator': TranslatorController(),
}


class MainMenu:
    _controllers: dict[str, MediaGrabberController | TranslatorController]

    def __init__(self, menu_items: dict[str, MediaGrabberController | TranslatorController]):
        self._controllers = menu_items

    def __str__(self):
        numbered_list = []
        for index, controller in enumerate(self._controllers.values()):
            numbered_list.append(f'{index + 1}. {controller.menu_title}')
        return '\n'.join(numbered_list)

    @property
    def max_index(self) -> int:
        """Returns the maximum allowed menu item number"""
        return len(self._controllers)

    @property
    def min_index(self) -> 0:
        """Returns the minimum allowed menu item number"""
        return 1 if not self.is_empty else 0

    @property
    def is_empty(self):
        """Checks if the menu is empty"""
        return True if not self._controllers else False

    def get_controller_by_index(self, controller_index: int) -> Controller | IndexError:
        if self.min_index <= controller_index <= self.max_index and controller_index > 0:
            return self._controllers.get(list(self._controllers.keys())[controller_index - 1])
        else:
            raise IndexError

    def get_controller_by_key(self, key: str) -> Controller | None:
        return self._controllers.get(key)

    def choose_controller(self, controller_key: str = None) -> Controller:
        print(f'\n{self}')
        controller = self.get_controller_by_key(controller_key) if controller_key else None
        while not controller:
            try:
                controller_index = int(
                    input(f'\nВыберите режим работы приложения [{self.min_index}-{self.max_index}]: ')
                )
                controller = self.get_controller_by_index(controller_index)
            except ValueError:
                print(
                    f'\n{Style.DIM}{Fore.LIGHTRED_EX}ВЫ ВВЕЛИ НЕКОРРЕКТНОЕ ЗНАЧЕНИЕ{Style.RESET_ALL}'
                    f'\nНеобходимо ввести число в диапазоне от {self.min_index} до {self.max_index}')
            except IndexError:
                print(
                    f'\n{Style.DIM}{Fore.LIGHTRED_EX}ПУНКТА МЕНЮ С ТАКИМ НОМЕРОМ НЕ СУЩЕСТВУЕТ{Style.RESET_ALL}'
                    f'\nНеобходимо ввести число в диапазоне от {self.min_index} до {self.max_index}')
        return controller


