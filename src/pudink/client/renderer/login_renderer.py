import pyglet

from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.controller.login_controller import LoginController
from pudink.client.pyglet.password_text_entry import PasswordTextEntry
from pudink.client.frontend.color_palette import ColorPalette


class LoginRenderer:
    def __init__(
        self,
        window: pyglet.window.Window,
        login: LoginController,
        asset_manager: AssetManager,
    ) -> None:
        self.login_controller = login
        self.window = window
        self.asset_manager = asset_manager

        self.batch = pyglet.graphics.Batch()
        self.background_group = pyglet.graphics.Group(0)
        self.foreground_group = pyglet.graphics.Group(1)

        self.background = asset_manager.get_background()
        self.background_sprite = pyglet.sprite.Sprite(
            self.background, x=0, y=0, batch=self.batch, group=self.background_group
        )

        self.title = pyglet.text.Label(
            "Pudink",
            x=window.width // 2,
            y=window.height // 2 + 200,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )

        self.state = pyglet.text.Label(
            "",
            x=window.width // 2,
            y=window.height // 2 - 200,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            multiline=True,
            width=window.width // 3,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )
        self.frame = pyglet.gui.Frame(self.window, order=2)
        self.pushbutton = pyglet.gui.PushButton(
            300,
            200,
            pressed=self.asset_manager.get_button_pressed(),
            depressed=self.asset_manager.get_button_depressed(),
            hover=self.asset_manager.get_button_hover(),
            batch=self.batch,
        )
        self.pushbutton.set_handler("on_release", self._login_handler)
        self.frame.add_widget(self.pushbutton)

        # This Widget is not added to the Frame. Because it is sensitive
        # to drag-and-select events falling outside the Frame's spatial hash,
        # it's best to let it handle Window events directly.
        self.username_label = pyglet.text.Label(
            "Username:",
            x=300,
            y=350,
            batch=self.batch,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )
        self.password_label = pyglet.text.Label(
            "Password:",
            x=300,
            y=300,
            batch=self.batch,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )

        self.username_entry = pyglet.gui.TextEntry(
            "",
            400,
            350,
            150,
            batch=self.batch,
            group=self.foreground_group,
            color=ColorPalette.LIGHT.value,
            text_color=ColorPalette.DARK.value,
            caret_color=ColorPalette.DARK.value,
        )
        self.username_entry.set_handler("on_commit", self.login_handler)

        self.password_entry = PasswordTextEntry(
            "",
            400,
            300,
            150,
            batch=self.batch,
            group=self.foreground_group,
            color=ColorPalette.LIGHT.value,
            text_color=ColorPalette.DARK.value,
            caret_color=ColorPalette.DARK.value,
        )
        self.password_entry.set_handler("on_commit", self.login_handler)

        self.login_controller.connect(
            self._on_connecting, self._on_success, self._on_fail
        )

    def on_draw(self) -> None:
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == pyglet.window.key.ENTER:
            self._login_handler()

    def before_scene_switch(self):
        self.window.remove_handlers()
        self.password_entry.enabled = False
        self.username_entry.enabled = False
        self.pushbutton.enabled = False

    def after_scene_switch(self, previous_scene):
        self.window.push_handlers(self.username_entry)
        self.window.push_handlers(self.password_entry)
        self.password_entry.enabled = True
        self.username_entry.enabled = True
        self.pushbutton.enabled = True

    def _on_connecting(self, data: str):
        print(data)
        self.state.text = data

    def _on_success(self, data: str):
        print(data)
        self.state.text = data

    def _on_fail(self, data: ConnectionError):
        print(data)
        self.state.text = data.message

    def login_handler(self, _):
        self._login_handler()

    def _login_handler(self):
        if not self.username_entry.value or not self.password_entry.value:
            return

        self.login_controller.login(
            self.username_entry.value,
            self.password_entry.get_password(),
            self._on_success,
            self._on_fail,
        )
