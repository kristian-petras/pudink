from typing import Callable, Optional

from pudink.client.controller.base_controller import BaseController
from pudink.client.game.client import ClientCallback
from pudink.common.model import ConnectionFailure


class TitleController(BaseController):
    """
    Controller class for the title screen.

    This class handles the logic and functionality of the title screen in the application.
    It provides methods for connecting to a server, handling connection events, and switching screens.

    Attributes:
        scene (str): The name of the scene.
        on_update_callback (Optional[Callable[[str], None]]): Callback function for update events.

    Methods:
        __init__(self, factory, scene_manager): Initializes the TitleController instance.
        connect(self, host: str, port: int) -> None: Connects to a server.
        _on_connecting(self, message: str) -> None: Handles the connecting event.
        _on_connect(self, message: str) -> None: Handles the connection success event.
        _on_disconnect(self, error: ConnectionFailure) -> None: Handles the connection failure event.
    """

    scene: str
    on_update_callback: Optional[Callable[[str], None]]

    def __init__(self, factory, scene_manager):
        super().__init__(factory, scene_manager, "title")
        self.on_update_callback = None

        self.register_callback(
            ClientCallback.STARTED_CONNECTING,
            self._on_connecting,
            self.scene,
        )
        self.register_callback(
            ClientCallback.CONNECTION_SUCCESS,
            self._on_connect,
            self.scene,
        )
        self.register_callback(
            ClientCallback.CONNECTION_FAILED,
            self._on_disconnect,
            self.scene,
        )

    def connect(self, host: str, port: int) -> None:
        """
        Connects to a server.

        Args:
            host (str): The host address of the server.
            port (int): The port number of the server.
        """
        print(f"Connecting to {host}:{port}")
        self._factory.connect(host, port)

    def _on_connecting(self, message: str) -> None:
        """
        Handles the connecting event.

        Args:
            message (str): The connecting message.
        """
        print(f"Connecting... {message}")
        if self.on_update_callback is not None:
            self.on_update_callback(message)

    def _on_connect(self, message: str) -> None:
        """
        Handles the connection success event.

        Args:
            message (str): The connection success message.
        """
        print(f"Connected: {message}")
        if self.on_update_callback is not None:
            self.on_update_callback(message)
        self.switch_screen("menu")

    def _on_disconnect(self, error: ConnectionFailure) -> None:
        """
        Handles the connection failure event.

        Args:
            error (ConnectionFailure): The connection failure error.
        """
        print(f"Disconnected: {error.message}")
        if self.on_update_callback is not None:
            self.on_update_callback(error.message)
