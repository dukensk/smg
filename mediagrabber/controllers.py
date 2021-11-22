from smg.controllers import Controller


class MediaGrabberController(Controller):

    @property
    def title(self) -> str:
        return 'Скачивание аудио и видео с YouTube, Twitch, Vimeo и т.п.'

    @property
    def menu_title(self) -> str:
        return 'Media Grabber'

    def main(self) -> bool:
        return True