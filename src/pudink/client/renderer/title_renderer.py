from pyglet.window import Window

from pudink.client.controller.title_controller import TitleController
from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.renderer.base_renderer import BaseRenderer


class TitleRenderer(BaseRenderer):
    def __init__(
        self,
        window: Window,
        asset_manager: AssetManager,
        controller: TitleController,
    ) -> None:
        super().__init__(window, asset_manager)
        self.controller = controller
        self.controller.on_update_callback = self._update_status_message
        self._title = self.create_sprite(
            texture=asset_manager.get_title(),
            x=window.width // 2,
            y=window.height // 2 + 100,
        )
        self._host_label = self.create_label(
            text="Host:",
            x=200,
            y=window.height // 2 + 10,
        )
        self._host = self.create_entry(
            text="localhost",
            x=250,
            y=window.height // 2,
            handler=self._connect_handler,
        )
        self._port_label = self.create_label(
            text="Port:",
            x=200,
            y=window.height // 2 - 30,
        )
        self._port = self.create_entry(
            text="8000",
            x=250,
            y=window.height // 2 - 40,
            handler=self._connect_handler,
        )
        self._button = self.create_button(
            x=window.width // 2 - 32,
            y=window.height // 2 - 90,
            handler=self._connect_handler_button,
        )
        self._status_message = self.create_label(
            text="",
            x=window.width // 2 - 100,
            y=window.height // 2 - 110,
            width=200,
            multiline=True,
            anchor_x="left",
            anchor_y="top",
            align="center",
        )

    def _connect_handler(self, text) -> None:
        self._connect_handler_button()

    def _connect_handler_button(self) -> None:
        if self._host.value and self._port.value:
            try:
                port = int(self._port.value)
            except ValueError:
                self._update_status_message("Port must be an integer")
                return
            self.controller.connect(self._host.value, port)

    def _update_status_message(self, message: str) -> None:
        print(f"Updating status message: {message}")
        self._status_message.text = message
