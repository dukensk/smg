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
                    input('\nВыберите режим работы приложения [{min_index}-{max_index}]: '
                          .format(min_index=self.min_index, max_index=self.max_index))
                )
                controller = self.get_controller_by_index(controller_index)
            except ValueError:
                print("Вы ввели некорректное значение. Необходимо ввести число в диапазоне от {min_index} до {max_index}"
                      .format(min_index=self.min_index, max_index=self.max_index))
            except IndexError:
                print('Пункта меню с таким номером не существует. Необходимо ввести число в диапазоне от {min_index} до {max_index}'
                      .format(min_index=self.min_index, max_index=self.max_index))
        return controller


class MainController(Controller):
    @property
    def title(self) -> str:
        return 'Выбор режима работы приложения'

    @property
    def menu_title(self) -> str:
        return self.title

    def run(self, controller_key: str = None) -> bool:
        while True:
            self.show_app_header()
            self.main(controller_key)
            controller_key = None
        return True

    def main(self, controller_key: str = None):
        controller = MainMenu(controllers).choose_controller(controller_key) if controller_key else MainMenu(controllers).choose_controller()
        controller.run()
