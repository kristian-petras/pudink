from pyglet.window import Window
from pudink.client.controller.menu_controller import MenuController
from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.renderer.base_renderer import BaseRenderer


class MenuRenderer(BaseRenderer):
    def __init__(
        self, window: Window, asset_manager: AssetManager, controller: MenuController
    ) -> None:
        super().__init__(window, asset_manager)
        self.controller = controller

        self._title = self.create_sprite(
            texture=asset_manager.get_title(),
            x=window.width // 2,
            y=window.height // 2 + 300,
        )
        self._username_label = self.create_label(
            text="Username:",
            x=200,
            y=window.height // 2 + 200,
        )
        self._username = self.create_entry(
            text="",
            x=250,
            y=window.height // 2 + 190,
            handler=self._connect_handler,
        )
        self._password_label = self.create_label(
            text="Password:",
            x=200,
            y=window.height // 2 + 160,
        )
        self._password = self.create_entry(
            text="",
            x=250,
            y=window.height // 2 + 150,
            handler=self._connect_handler,
        )
        self._button = self.create_button(
            x=window.width // 2 - 32,
            y=window.height // 2 - 140,
            handler=self._connect_handler_button,
        )
        self._button_label = self.create_label(
            text="Login/Register:",
            x=window.width // 2,
            y=window.height // 2 - 80,
        )
        self._status_message = self.create_label(
            text="",
            x=window.width // 2 - 100,
            y=window.height // 2 + 90,
            width=200,
            multiline=True,
            anchor_x="left",
            anchor_y="top",
            align="center",
        )

        self.head_counter = 1
        self.head = self.create_sprite(
            texture=asset_manager.get_head(self.head_counter),
            x=window.width // 2,
            y=window.height // 2 + 96,
        )

        self.body_counter = 1
        self.body = self.create_sprite(
            texture=asset_manager.get_body(self.body_counter),
            x=window.width // 2,
            y=window.height // 2,
        )

        self.right_button_head = self.create_button(
            x=window.width // 2 + 64,
            y=window.height // 2 + 64,
            handler=self._next_head,
            pressed=asset_manager.get_right(),
            depressed=asset_manager.get_right(),
            hover=asset_manager.get_right(),
        )

        self.right_button_body = self.create_button(
            x=window.width // 2 + 64,
            y=window.height // 2,
            handler=self._next_body,
            pressed=asset_manager.get_right(),
            depressed=asset_manager.get_right(),
            hover=asset_manager.get_right(),
        )

        self.left_button_head = self.create_button(
            x=window.width // 2 - 96,
            y=window.height // 2 + 64,
            handler=self._previous_head,
            pressed=asset_manager.get_left(),
            depressed=asset_manager.get_left(),
            hover=asset_manager.get_left(),
        )

        self.left_button_body = self.create_button(
            x=window.width // 2 - 96,
            y=window.height // 2,
            handler=self._previous_body,
            pressed=asset_manager.get_left(),
            depressed=asset_manager.get_left(),
            hover=asset_manager.get_left(),
        )

    def _connect_handler(self, text) -> None:
        self._connect_handler_button()

    def _connect_handler_button(self) -> None:
        print("Connecting")

    def _next_head(self) -> None:
        self.head_counter += 1
        if self.head_counter > 5:
            self.head_counter = 1
        self.head.delete()
        self.head = self.create_sprite(
            texture=self.asset_manager.get_head(self.head_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 + 96,
        )

    def _next_body(self) -> None:
        self.body_counter += 1
        if self.body_counter > 5:
            self.body_counter = 1
        self.body.delete()
        self.body = self.create_sprite(
            texture=self.asset_manager.get_body(self.body_counter),
            x=self.window.width // 2,
            y=self.window.height // 2,
        )

    def _previous_head(self) -> None:
        self.head_counter -= 1
        if self.head_counter < 1:
            self.head_counter = 5
        self.head.delete()
        self.head = self.create_sprite(
            texture=self.asset_manager.get_head(self.head_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 + 96,
        )

    def _previous_body(self) -> None:
        self.body_counter -= 1
        if self.body_counter < 1:
            self.body_counter = 5
        self.body.delete()
        self.body = self.create_sprite(
            texture=self.asset_manager.get_body(self.body_counter),
            x=self.window.width // 2,
            y=self.window.height // 2,
        )
