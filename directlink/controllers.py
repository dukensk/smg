from common.controllers import Controller
from common.notifications import show_push_notification
from directlink.downloaders import DirectLinkDownloader


class DirectLinkController(Controller):

    @property
    def header(self):
        return f'DIRECTLINK ❯❯ {super(DirectLinkController, self).header}'

    @property
    def title(self) -> str:
        return 'Скачивание файла по прямой ссылке'

    def main(self) -> bool:
        downloader = DirectLinkDownloader()
        file = downloader.download()

        if file:
            file.move_to_downloads()
            print(f'\nИнформация о файле: {file.info}')
            show_push_notification('SMG DIRECTLINK', f'Скачан файл: {file.name_with_extension} [{file.formatted_size}]')
            return True
        else:
            show_push_notification('SMG DIRECTLINK', f'Не удалось скачать файл по прямой ссылке: {downloader.url}')
            return False
