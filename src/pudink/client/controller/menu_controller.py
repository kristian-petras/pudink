from pudink.client.controller.base_controller import BaseController
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


class MenuController(BaseController):
    def __init__(
        self, factory: PudinkClientFactory, scene_manager: SceneManager
    ) -> None:
        super().__init__(factory, scene_manager)
        self.scene = "menu"

        self.factory.registerCallback(
            ClientCallback.CONNECTION_FAILED,
            self._on_disconnect,
            self.scene,
        )

    def _on_disconnect(self, message: str) -> None:
        print(f"Disconnected, switching to title screen: {message}")
        self.switch_screen("title")
        self.factory.process_callback(ClientCallback.CONNECTION_FAILED, message)

    def register(
        self,
        username: str,
        password: str,
        head_id: int,
        body_id: int,
    ) -> None:
        pass

    def login(self, username: str, password: str) -> None:
        pass
