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
            password=True,
        )

        self._login_button = self.create_button(
            x=window.width // 2 - 32,
            y=window.height // 2 + 80,
            handler=self._login_handler,
        )
        self._login_button_label = self.create_label(
            text="Login:",
            x=window.width // 2,
            y=window.height // 2 + 130,
        )

        self._status_message = self.create_label(
            text="",
            x=window.width // 2 - 100,
            y=window.height // 2 - 200,
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
            y=window.height // 2 + 46,
        )

        self.body_counter = 1
        self.body = self.create_sprite(
            texture=asset_manager.get_body(self.body_counter),
            x=window.width // 2,
            y=window.height // 2 - 50,
        )

        self.right_button_head = self.create_button(
            x=window.width // 2 + 64,
            y=window.height // 2 + 14,
            handler=self._next_head,
            pressed=asset_manager.get_right(),
            depressed=asset_manager.get_right(),
            hover=asset_manager.get_right(),
        )

        self.right_button_body = self.create_button(
            x=window.width // 2 + 64,
            y=window.height // 2 - 50,
            handler=self._next_body,
            pressed=asset_manager.get_right(),
            depressed=asset_manager.get_right(),
            hover=asset_manager.get_right(),
        )

        self.left_button_head = self.create_button(
            x=window.width // 2 - 96,
            y=window.height // 2 + 14,
            handler=self._previous_head,
            pressed=asset_manager.get_left(),
            depressed=asset_manager.get_left(),
            hover=asset_manager.get_left(),
        )

        self.left_button_body = self.create_button(
            x=window.width // 2 - 96,
            y=window.height // 2 - 50,
            handler=self._previous_body,
            pressed=asset_manager.get_left(),
            depressed=asset_manager.get_left(),
            hover=asset_manager.get_left(),
        )
        self._register_button = self.create_button(
            x=window.width // 2 - 32,
            y=window.height // 2 - 170,
            handler=self._register_handler,
        )
        self._register_button_label = self.create_label(
            text="Register:",
            x=window.width // 2,
            y=window.height // 2 - 120,
        )

        self.controller.on_fail_callback = self._on_fail

    def _login_handler(self) -> None:
        self.controller.login(self._username.value, self._password.value)

    def _register_handler(self) -> None:
        self.controller.register(
            self._username.value,
            self._password.value,
            self.head_counter,
            self.body_counter,
        )

    def _next_head(self) -> None:
        """
        Switches to the next head texture. Cycles over to the first head texture if the current head texture is the last one.
        """
        self.head_counter += 1
        if self.head_counter > 5:
            self.head_counter = 1
        self.head.delete()
        self.head = self.create_sprite(
            texture=self.asset_manager.get_head(self.head_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 + 46,
        )

    def _next_body(self) -> None:
        """
        Switches to the next body texture. Cycles over to the first body texture if the current body texture is the last one.
        """
        self.body_counter += 1
        if self.body_counter > 5:
            self.body_counter = 1
        self.body.delete()
        self.body = self.create_sprite(
            texture=self.asset_manager.get_body(self.body_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 - 50,
        )

    def _previous_head(self) -> None:
        """
        Switches to the previous head texture. Cycles over to the last head texture if the current head texture is the first one.
        """
        self.head_counter -= 1
        if self.head_counter < 1:
            self.head_counter = 5
        self.head.delete()
        self.head = self.create_sprite(
            texture=self.asset_manager.get_head(self.head_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 + 46,
        )

    def _previous_body(self) -> None:
        """
        Switches to the previous body texture. Cycles over to the last body texture if the current body texture is the first one.
        """
        self.body_counter -= 1
        if self.body_counter < 1:
            self.body_counter = 5
        self.body.delete()
        self.body = self.create_sprite(
            texture=self.asset_manager.get_body(self.body_counter),
            x=self.window.width // 2,
            y=self.window.height // 2 - 50,
        )

    def _on_fail(self, message: str) -> None:
        self._status_message.text = message