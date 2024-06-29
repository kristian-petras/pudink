import pyglet

from pudink.client.controller.login_controller import LoginController
from pudink.client.pyglet.password_text_entry import PasswordTextEntry


class LoginRenderer:
    def __init__(self, window: pyglet.window.Window, login: LoginController) -> None:
        self.window = window
        self.login_controller = login
        self.counter = 0
        self.batch = pyglet.graphics.Batch()
        self.title = pyglet.text.Label(
            "Pudink",
            x=window.width // 2,
            y=window.height // 2 + 200,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            color=(0, 0, 0, 255),
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
            color=(0, 0, 0, 255),
        )
        self.frame = pyglet.gui.Frame(self.window)

        depressed = pyglet.resource.image("blue_button04.png")
        pressed = pyglet.resource.image("blue_button05.png")
        hover = pyglet.resource.image("blue_button05.png")

        self.pushbutton = pyglet.gui.PushButton(
            300,
            200,
            pressed=pressed,
            depressed=depressed,
            hover=hover,
            batch=self.batch,
        )
        self.pushbutton.set_handler("on_release", self._login_handler)
        self.frame.add_widget(self.pushbutton)

        # This Widget is not added to the Frame. Because it is sensitive
        # to drag-and-select events falling outside the Frame's spatial hash,
        # it's best to let it handle Window events directly.
        self.username_label = pyglet.text.Label(
            "Username:", x=300, y=350, batch=self.batch, color=(0, 0, 0, 255)
        )
        self.password_label = pyglet.text.Label(
            "Password:", x=300, y=300, batch=self.batch, color=(0, 0, 0, 255)
        )

        self.username_entry = pyglet.gui.TextEntry("", 400, 350, 150, batch=self.batch)
        self.username_entry.set_handler("on_commit", self.login_handler)

        self.password_entry = PasswordTextEntry("", 400, 300, 150, batch=self.batch)
        self.password_entry.set_handler("on_commit", self.login_handler)

        self.window.push_handlers(self.username_entry)
        self.window.push_handlers(self.password_entry)

        self.login_controller.connect(
            self._on_connecting, self._on_success, self._on_fail
        )

    def on_draw(self) -> None:
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == pyglet.window.key.ENTER:
            self._login_handler()

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
