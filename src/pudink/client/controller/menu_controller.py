from typing import Any, Callable

from pudink.client.controller.base_controller import BaseController
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.game.client import ClientCallback
from pudink.client.game.client_factory import PudinkClientFactory
from pudink.client.game.world_state import WorldState
from pudink.common.model import (
    Character,
    ConnectionFailure,
    Credentials,
    NewAccount,
    PlayerSnapshot,
)


class MenuController(BaseController):
    """
    Controller class for the menu screen.

    This class handles user interactions and events on the menu screen,
    such as registering a new account, logging in, and processing received data.

    Attributes:
        on_fail_callback (Optional[Callable[[str], None]]): Optional callback function
            to be called when a connection failure occurs.
        _world_state (WorldState): The current state of the game world.
        factory (PudinkClientFactory): The client factory used for network communication.
        scene_manager (SceneManager): The scene manager for managing different screens.

    Args:
        factory (PudinkClientFactory): The client factory used for network communication.
        scene_manager (SceneManager): The scene manager for managing different screens.
        world_state (WorldState): The current state of the game world.

    """

    on_fail_callback: Callable[[str], None] | None
    _world_state: WorldState
    factory: PudinkClientFactory
    scene_manager: SceneManager

    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        world_state: WorldState,
    ) -> None:
        super().__init__(factory, scene_manager, "menu")
        self.on_fail_callback = None
        self._world_state = world_state

        self._factory.register_callback(
            ClientCallback.CONNECTION_FAILED,
            self._on_disconnect,
            self.scene,
        )

        self._factory.register_callback(
            ClientCallback.DATA_RECEIVED,
            self._on_data_received,
            self.scene,
        )

    def _on_disconnect(self, message: str) -> None:
        """
        Callback function called when a connection failure occurs.

        This function switches to the title screen and processes the connection failure.

        Args:
            message (str): The error message associated with the connection failure.

        Returns:
            None
        """
        print(f"Disconnected, switching to title screen: {message}")
        self.switch_screen("title")
        self._factory.process_callback(ClientCallback.CONNECTION_FAILED, message)

    def register(
        self,
        username: str,
        password: str,
        head_id: int,
        body_id: int,
    ) -> None:
        """
        Registers a new account with the provided username, password, head ID, and body ID.

        Args:
            username (str): The username for the new account.
            password (str): The password for the new account.
            head_id (int): The ID of the selected head.
            body_id (int): The ID of the selected body.

        Returns:
            None
        """
        self.send_message(NewAccount(username, password, Character(head_id, body_id)))

    def login(self, username: str, password: str) -> None:
        """
        Logs in the user with the provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            None
        """
        self.send_message(Credentials(username, password))

    def _on_data_received(self, data: Any) -> None:
        """
        Callback function called when data is received from the server.

        This function processes the received data, handling connection failures
        and updating the game world state.

        When the handshake is successful, the screen is switched to the world screen.

        Args:
            data (Any): The received data.

        Returns:
            None
        """
        if isinstance(data, ConnectionFailure):
            if self.on_fail_callback is not None:
                self.on_fail_callback(data.message)
            else:
                print(f"Received connection failure but no callback: {data.message}")
        elif isinstance(data, PlayerSnapshot):
            self._world_state.initialize_world(data)
            self.switch_screen("world")
