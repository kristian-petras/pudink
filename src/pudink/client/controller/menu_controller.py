from pudink.client.controller.base_controller import BaseController
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.model.world_state import WorldState
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory
from pudink.common.model import (
    Character,
    ConnectionFailure,
    Credentials,
    NewAccount,
    PlayerSnapshot,
)


class MenuController(BaseController):
    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        world_state: WorldState,
    ) -> None:
        super().__init__(factory, scene_manager)
        self.scene = "menu"
        self.on_fail_callback = None
        self._world_state = world_state

        self.factory.registerCallback(
            ClientCallback.CONNECTION_FAILED,
            self._on_disconnect,
            self.scene,
        )

        self.factory.registerCallback(
            ClientCallback.DATA_RECEIVED,
            self._on_data_received,
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
        self.send_message(NewAccount(username, password, Character(head_id, body_id)))

    def login(self, username: str, password: str) -> None:
        self.send_message(Credentials(username, password))

    def _on_data_received(self, data: any) -> None:
        if type(data) == ConnectionFailure:
            self.on_fail_callback(data.message)
        elif type(data) == PlayerSnapshot:
            self._world_state.initialize_world(data)
            self.switch_screen("world")
