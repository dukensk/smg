from common.controllers import Controller
from common.menu import FactoryMenu, MenuItem
from directlink.controllers import DirectLinkController
from info.controllers import InfoController
from mediagrabber.controllers import MediaGrabberController
from translator.controllers import TranslatorController

controllers = {
    'mediagrabber': MenuItem('Mediagrabber', MediaGrabberController),
    'translator': MenuItem('Translator', TranslatorController),
    'directlink': MenuItem('Скачивание файла по прямой ссылке', DirectLinkController),
    'info': MenuItem('Получение информации о медиафайле', InfoController),
}


class MainMenu(FactoryMenu):

    @property
    def _input_message(self) -> str:
        return 'Выберите режим работы приложения'

    def choose(self, item_key: str = None) -> Controller:
        return super(MainMenu, self).choose(item_key)
