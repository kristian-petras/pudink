from enum import Enum
from typing import Callable
import pyglet

from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


class LoginController:
    def __init__(self, factory: PudinkClientFactory, scene_manager) -> None:
        self.factory = factory
        self.scene_manager = scene_manager

    def login(
        self,
        on_connecting: Callable[[], None],
        on_success: Callable[[], None],
        on_fail: Callable[[], None],
    ) -> None:
        self.factory.registerCallback(ClientCallback.STARTED_CONNECTING, on_connecting)
        self.factory.registerCallback(ClientCallback.CONNECTION_FAILED, on_fail)
        self.factory.registerCallback(ClientCallback.CONNECTION_SUCCESS, on_success)
        self.factory.connect()

    def switch_screen(self, scene):
        self.factory.set_scene(scene)
        self.scene_manager.switch_to_scene(scene)


class LoginRenderer:
    def __init__(self, window: pyglet.window.Window, login: LoginController) -> None:
        self.window = window
        self.login = login
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

    def on_draw(self) -> None:
        self.window.clear()
        self.label.text = f"Login Screen {self.counter}"
        self.counter += 1
        self.batch.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == pyglet.window.key.ENTER:
            self.login.login(self._on_connecting, self._on_success, self._on_fail)
        elif symbol == pyglet.window.key.ESCAPE:
            self.login.switch_screen("main")

    def _on_connecting(self):
        print("connecting")
        self.state.text = "Connecting"

    def _on_success(self):
        print("success")
        self.state.text = "Connected"

    def _on_fail(self):
        print("fail")
        self.state.text = "Failed"


# Renderer -> on keypress -> login.login()
