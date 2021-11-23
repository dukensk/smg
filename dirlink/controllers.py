from common.controllers import Controller
from dirlink.downloaders import DirectLinkDownloader


class DirectLinkController(Controller):

    @property
    def title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    @property
    def menu_title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    def main(self) -> bool:
        file = DirectLinkDownloader().download()
        return True if file else False
