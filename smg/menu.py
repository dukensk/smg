from common.controllers import Controller
from common.menu import FactoryMenu, MenuItem
from directlink.controllers import DirectLinkController
from mediagrabber.controllers import MediaGrabberController
from translator.controllers import TranslatorController

controllers = {
    'mediagrabber': MenuItem('Mediagrabber', MediaGrabberController),
    'translator': MenuItem('Translator', TranslatorController),
    'directlink': MenuItem('Скачивание файла по прямой ссылке', DirectLinkController),
}


class MainMenu(FactoryMenu):

    @property
    def _input_message(self) -> str:
        return 'Выберите режим работы приложения'

    def choose(self, item_key: str = None) -> Controller:
        return super(MainMenu, self).choose(item_key)
