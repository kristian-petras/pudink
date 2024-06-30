from typing import Callable, Optional
from pudink.client.controller.base_controller import BaseController
from pudink.client.protocol.factory import ClientCallback
from pudink.common.model import ConnectionError


class TitleController(BaseController):
    scene: str
    on_update_callback: Optional[Callable[[str], None]]

    def __init__(self, factory, scene_manager):
        super().__init__(factory, scene_manager)
        self.scene = "title"
        self.on_update_callback = None

        self.factory.registerCallback(
            ClientCallback.STARTED_CONNECTING,
            self._on_connecting,
            self.scene,
        )
        self.factory.registerCallback(
            ClientCallback.CONNECTION_SUCCESS,
            self._on_connect,
            self.scene,
        )
        self.factory.registerCallback(
            ClientCallback.CONNECTION_FAILED,
            self._on_disconnect,
            self.scene,
        )

    def connect(self, host: str, port: int) -> None:
        print(f"Connecting to {host}:{port}")
        self.factory.connect(host, port)

    def _on_connecting(self, message: str) -> None:
        print(f"Connecting... {message}")
        if self.on_update_callback is not None:
            self.on_update_callback(message)

    def _on_connect(self, message: str) -> None:
        print(f"Connected: {message}")
        if self.on_update_callback is not None:
            self.on_update_callback(message)
        self.switch_screen("menu")

    def _on_disconnect(self, error: ConnectionError) -> None:
        print(f"Disconnected: {error.message}")
        if self.on_update_callback is not None:
            self.on_update_callback(error.message)
