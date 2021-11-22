from common.controllers import Controller
from translator.downloaders import VoiceOverDownloader


class TranslatorController(Controller):

    @property
    def title(self) -> str:
        return 'Перевод аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    @property
    def menu_title(self) -> str:
        return 'Translator'

    def main(self) -> bool:
        downloader = VoiceOverDownloader()
        # voiceover = downloader.download()
        return True
