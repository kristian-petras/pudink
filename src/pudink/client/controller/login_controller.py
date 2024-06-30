from pudink.client.controller.base_controller import BaseController
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.model.world_state import WorldState
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


from typing import Callable

from pudink.common.model import Credentials, ConnectionError, PlayerSnapshot


class LoginController(BaseController):
    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        world_state: WorldState,
    ) -> None:
        super().__init__(factory, scene_manager)
        self.world_state = world_state
        self.scene = "login"

    def connect(
        self,
        on_connecting: Callable[[str], None],
        on_success: Callable[[str], None],
        on_fail: Callable[[ConnectionError], None],
    ) -> None:
        self.factory.registerCallback(
            ClientCallback.STARTED_CONNECTING,
            on_connecting,
            self.scene,
        )
        self.factory.registerCallback(
            ClientCallback.CONNECTION_FAILED,
            on_fail,
            self.scene,
        )
        self.factory.registerCallback(
            ClientCallback.CONNECTION_SUCCESS,
            on_success,
            self.scene,
        )

    def login(
        self,
        username: str,
        password: str,
        on_success: Callable[[str], None],
        on_fail: Callable[[ConnectionError], None],
    ) -> None:
        if not self.factory.connected:
            self.factory.connect()
            if not self.factory.connected:
                return

        self.factory.registerCallback(
            ClientCallback.DATA_RECEIVED,
            lambda response: self._on_login_response(response, on_success, on_fail),
            self.scene,
        )
        credentials = Credentials(username, password)
        self.send_message(credentials)

    # After client sends credentials, receive initialization data from server
    def _on_login_response(
        self,
        data: any,
        on_success: Callable[[str], None],
        on_fail: Callable[[ConnectionError], None],
    ) -> None:
        if type(data) == ConnectionError:
            on_fail(data)
        elif type(data) == PlayerSnapshot:
            success = f"Switching to world screen, players online: {len(data.players)}"
            print(success)
            print(data)
            on_success(success)
            self.world_state.initialize_world(data)
            self.switch_screen("world")
        else:
            fail = f"Received unexpected message: {data}"
            print(fail)
            on_fail(ConnectionError(fail))
