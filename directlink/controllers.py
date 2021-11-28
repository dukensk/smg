from common.controllers import Controller
from directlink.downloaders import DirectLinkDownloader


class DirectLinkController(Controller):

    @property
    def title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    @property
    def menu_title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    def main(self) -> bool:
        file = DirectLinkDownloader().download()
        file.move_to_downloads()
        print(f'\nИнформация о файле: {file.info}')
        return True if file else False
