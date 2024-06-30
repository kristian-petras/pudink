from pudink.client.controller.base_controller import BaseController
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.factory import PudinkClientFactory


class MenuController(BaseController):
    def __init__(
        self, factory: PudinkClientFactory, scene_manager: SceneManager
    ) -> None:
        super().__init__(factory, scene_manager)
        self.scene = "menu"
