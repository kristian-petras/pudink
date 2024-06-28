from enum import Enum
import pyglet

from pudink.client.controller.login_controller import LoginController


class LoginRenderer:
    def __init__(self, window: pyglet.window.Window, login: LoginController) -> None:
        self.window = window
        self.login_controller = login
        self.counter = 0
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            "Login Screen",
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.state = pyglet.text.Label(
            "State",
            x=window.width // 2,
            y=window.height // 2 - 50,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.name = "tino"

    def on_draw(self) -> None:
        self.window.clear()
        self.label.text = f"Login Screen {self.counter}"
        self.counter += 1
        self.batch.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == pyglet.window.key.ENTER:
            data = {"name": self.name, "password": "password"}
            self.login_controller.login(
                data, self._on_connecting, self._on_success, self._on_fail
            )

    def _on_connecting(self, data: str):
        print("connecting")
        self.state.text = data

    def _on_success(self, data: str):
        print("success")
        self.state.text = data

    def _on_fail(self, data: str):
        print(data)
        self.state.text = "Connection failed"
