from common.controllers import Controller
from smg.main import MainMenu, controllers


class MainController(Controller):
    """Application main controller"""

    @property
    def title(self) -> str:
        return 'Выбор режима работы приложения'

    @property
    def menu_title(self) -> str:
        return self.title

    def run(self, controller_key: str = None):
        while True:
            self.show_app_header()
            self.main(controller_key)
            controller_key = None

    def main(self, controller_key: str = None):
        controller = MainMenu(controllers).choose_controller(controller_key)
        controller.run()
