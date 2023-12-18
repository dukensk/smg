from colorama import Style, Fore

from common.controllers import Controller
from common.notifications import show_push_notification
from translator.downloaders import VoiceOverDownloader, TranslatableMediaDownloader
from translator.media import VoiceOver, TranslatableVideoFile, TranslatableAudioFile


class TranslatorController(Controller):

    @property
    def header(self):
        return f'{Fore.LIGHTMAGENTA_EX}TRANSLATOR ❯❯{Style.RESET_ALL} {super(TranslatorController, self).header}'

    @property
    def title(self) -> str:
        return 'Перевод аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    def main(self) -> bool:
        media_downloader, voiceover_downloader = self._get_downloaders()
        media_file, voiceover = self._download_media_files(media_downloader, voiceover_downloader)
        voiceover.preprocess(media_file.audio_sample_rate)

        if media_file:
            media_file.add_voiceover(voiceover)
            media_file.move_to_downloads()
            self.show_app_header()
            print(f'\n{media_downloader.info}')
            print(f'\n{Style.NORMAL}{Fore.LIGHTGREEN_EX}ВСЕ ОПЕРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ{Style.RESET_ALL}')
            print(f'Переведен медиафайл: {media_file.info}')
            show_push_notification('Переведен медиафайл',
                                   f'{media_file.name_with_extension} [{media_file.formatted_size}]',
                                   'translator_icon.ico', 'SMG: TRANSLATOR')
            return True
        else:
            show_push_notification('Не удалось перевести',
                                   f'{media_downloader.metadata.title}', 'translator_icon.ico', 'SMG: TRANSLATOR')
            return False

    def _get_downloaders(self) -> tuple[TranslatableMediaDownloader, VoiceOverDownloader]:
        media_downloader = TranslatableMediaDownloader()
        self.show_app_header()
        print('\nПолучаем метаданные...')
        info = media_downloader.info
        self.show_app_header()
        print(f'\n{info}')
        voiceover_downloader = VoiceOverDownloader()
        self.show_app_header()
        print(f'\n{info}\n')
        return media_downloader, voiceover_downloader

    def _download_media_files(self, media_downloader: TranslatableMediaDownloader, voiceover_downloader: VoiceOverDownloader) \
            -> tuple[TranslatableAudioFile | TranslatableVideoFile, VoiceOver]:
        voiceover = voiceover_downloader.download()
        if voiceover:
            print('\nСкачиваем медиафайл...')
            media_file = media_downloader.download()
        else:
            media_file = None
            print(f'{Style.RESET_ALL}{Style.NORMAL}{Fore.RED}  \n\nYOU DIED{Style.RESET_ALL}')
            print('\nБез закадрового перевода нет смысла качать видео. :('
                  '\nПопробуйте скачать что-то еще.')
            print(f'Проблемное  видео: {media_downloader.url}')
        return media_file, voiceover
