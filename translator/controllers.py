from colorama import Style, Fore

from common.controllers import Controller
from translator.downloaders import VoiceOverDownloader, TranslatableMediaDownloader
from translator.media import VoiceOver, TranslatableVideoFile, TranslatableAudioFile


class TranslatorController(Controller):

    @property
    def title(self) -> str:
        return 'Перевод аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    @property
    def menu_title(self) -> str:
        return 'Translator'

    def main(self) -> bool:
        media_downloader, voiceover_downloader = self._get_downloaders()
        media_file, voiceover = self._download_media_files(media_downloader, voiceover_downloader)
        if media_file:
            media_file.add_voiceover(voiceover)
            media_file.move_to_downloads()
            print(f'Скачан медиафайл: {media_file.info}')
            return True
        else:
            return False

    def _get_downloaders(self) -> tuple[TranslatableMediaDownloader, VoiceOverDownloader]:
        media_downloader = TranslatableMediaDownloader()
        self.show_app_header()
        print('\nПолучаем метаданные...')
        info = media_downloader.info
        self.show_app_header()
        print(f'\n{info}\n')
        voiceover_downloader = VoiceOverDownloader()
        self.show_app_header()
        print(f'\n{info}\n')
        return media_downloader, voiceover_downloader

    def _download_media_files(self, media_downloader: TranslatableMediaDownloader, voiceover_downloader: VoiceOverDownloader) \
            -> tuple[TranslatableAudioFile | TranslatableVideoFile, VoiceOver]:
        voiceover = voiceover_downloader.download()
        if voiceover:
            media_file = media_downloader.download()
        else:
            media_file = None
            print(f'{Style.DIM}{Fore.RED}  \n\nYOU DIED{Style.RESET_ALL}')
            print('\nБез закадрового перевода нет смысла качать видео. :('
                  '\nПопробуйте скачать что-то еще.')
            print(f'Проблемное  видео: {media_downloader.url}')
        return media_file, voiceover
