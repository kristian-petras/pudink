from pudink.client.asset_manager import AssetManager
from pudink.client.controller.title_controller import TitleController
from pudink.client.renderer.base_renderer import BaseRenderer
from pyglet.window import Window
from pyglet.text import Label
from pyglet.gui import TextEntry, PushButton

from pudink.client.renderer.color_palette import ColorPalette


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
        self._title = self.create_label(
            text="Pudink",
            x=window.width // 2,
            y=window.height // 2 + 200,
        )
        self._host_label = self.create_label(
            text="Host:",
            x=250,
            y=window.height // 2 + 110,
        )
        self._host = self.create_entry(
            text="localhost",
            x=300,
            y=window.height // 2 + 100,
            handler=self._connect_handler,
        )
        self._port_label = self.create_label(
            text="Port:",
            x=250,
            y=window.height // 2 + 70,
        )
        self._port = self.create_entry(
            text="8000",
            x=300,
            y=window.height // 2 + 60,
            handler=self._connect_handler,
        )
        self._button = self.create_button(
            x=300,
            y=window.height // 2 + 10,
            handler=self._connect_handler_button,
        )
        self._status_message = self.create_label(
            text="",
            x=window.width // 2,
            y=window.height // 2 - 50,
            width=window.width // 3,
            multiline=True,
            anchor_x="left",
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
