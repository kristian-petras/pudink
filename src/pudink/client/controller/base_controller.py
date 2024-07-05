from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.client_factory import PudinkClientFactory
from pudink.client.protocol.client import ClientCallback


from typing import Any, Callable


class BaseController:
    scene: str
    _factory: PudinkClientFactory
    _scene_manager: SceneManager

    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        scene: str,
    ) -> None:
        self._factory = factory
        self._scene_manager = scene_manager
        self.scene = scene

    def switch_screen(self, scene: str) -> None:
        self._factory.set_scene(scene)
        self._scene_manager.switch_to_scene(scene)

    def send_message(self, data: Any) -> None:
        if self._factory.client is not None:
            self._factory.client.send_message(data)
        else:
            print(f"Client not connected, cannot send message {data}")

    def register_callback(
        self,
        callback: ClientCallback,
        function: Callable[[Any], None],
        scene: str,
    ):
        self._factory.register_callback(callback, function, scene)
