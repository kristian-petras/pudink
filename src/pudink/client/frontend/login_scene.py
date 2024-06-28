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
        on_connecting: Callable[[str], None],
        on_success: Callable[[str], None],
        on_fail: Callable[[str], None],
    ) -> None:
        self.factory.registerCallback(ClientCallback.STARTED_CONNECTING, on_connecting)
        self.factory.registerCallback(ClientCallback.CONNECTION_FAILED, on_fail)
        self.factory.registerCallback(
            ClientCallback.CONNECTION_SUCCESS,
            lambda data: self._on_success(on_success, data),
        )
        self.factory.registerCallback(
            ClientCallback.DATA_RECEIVED, self._on_initialization
        )
        self.factory.connect()

    def switch_screen(self, scene):
        self.factory.set_scene(scene)
        self.scene_manager.switch_to_scene(scene)

    def _on_success(self, renderer_on_success: Callable[[str], None], data: str):
        self.factory.client.send_message("login")
        renderer_on_success(data)

    def _on_initialization(self, data):
        print(data)
        print("initialized")
        self.switch_screen("main")


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

    def _on_connecting(self, data: str):
        print("connecting")
        self.state.text = data

    def _on_success(self, data: str):
        print("success")
        self.state.text = data

    def _on_fail(self, data: str):
        print("fail")
        self.state.text = data
