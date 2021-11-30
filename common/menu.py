from dataclasses import dataclass
from typing import Type

from colorama import Style, Fore


@dataclass
class MenuItem:
    label: str = None
    object_type: Type = None


class FactoryMenu:
    """Factory menu that creates objects corresponding to the selected item"""
    _items: dict[str, MenuItem]

    def __init__(self, items: dict[str, MenuItem] = None):
        if items is None:
            items = []
        self._items = items

    def __len__(self):
        return len(self._items)

    @property
    def is_empty(self):
        """Checks if the menu is empty"""
        return True if not len(self) else False

    @property
    def max_index(self) -> int:
        """Returns the maximum allowed menu item number"""
        return len(self)

    @property
    def min_index(self) -> int:
        """Returns the minimum allowed menu item number"""
        return 1 if not self.is_empty else 0

    @property
    def _input_message(self) -> str:
        """The message that appears when entering the menu item number"""
        return f'Выберите пункт меню'

    def __str__(self):
        numbered_list = []
        for index, item in enumerate(self._items.values()):
            numbered_list.append(f'{index + 1}. {item.label}')
        return '\n'.join(numbered_list)

    def _get_item_by_index(self, index: int) -> MenuItem | IndexError:
        if self.min_index <= index <= self.max_index and index > 0:
            return self._items.get(list(self._items.keys())[index - 1])
        else:
            raise IndexError

    def _get_item_by_key(self, key: str) -> MenuItem | None:
        """Gets a menu item by key"""
        return self._items.get(key)

    def _choose_item(self) -> MenuItem:
        try:
            item_index = int(
                input(f'\n{self._input_message} [{self.min_index}-{self.max_index}]: ')
            )
            item = self._get_item_by_index(item_index)
            return item
        except ValueError:
            print(
                f'\n{Style.DIM}{Fore.LIGHTRED_EX}ВЫ ВВЕЛИ НЕКОРРЕКТНОЕ ЗНАЧЕНИЕ{Style.RESET_ALL}'
                f'\nНеобходимо ввести число в диапазоне от {self.min_index} до {self.max_index}')
        except IndexError:
            print(
                f'\n{Style.DIM}{Fore.LIGHTRED_EX}ПУНКТА МЕНЮ С ТАКИМ НОМЕРОМ НЕ СУЩЕСТВУЕТ{Style.RESET_ALL}'
                f'\nНеобходимо ввести число в диапазоне от {self.min_index} до {self.max_index}')

    def _create_instance(self, object_type: Type):
        """
        Creates an instance of an object
        :param object_type: тип создаваемого объекта
        :return:
        """
        return object_type()

    def choose(self, item_key: str = None):
        """Selecting a menu item"""
        print(f'\n{self}')
        item = self._get_item_by_key(item_key) if item_key else None

        while not item:
            item = self._choose_item()

        return self._create_instance(item.object_type)
