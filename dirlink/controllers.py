from common.controllers import Controller


class DirectLinkController(Controller):

    @property
    def title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    @property
    def menu_title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    def main(self) -> bool:
        return True