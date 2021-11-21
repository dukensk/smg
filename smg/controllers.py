from abc import ABC, abstractmethod


class Controller(ABC):
    """Base abstract controller class"""

    APP_HEADER: str = 'Simple Media Grabber by Duke'

    @abstractmethod
    def run(self) -> bool:
        """Run Controller"""

    def show_app_header(self):
        """Shows the title of the application"""
        print(self.APP_HEADER)
