from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.client_factory import PudinkClientFactory
from pudink.client.protocol.client import ClientCallback


from typing import Any, Callable


class BaseController:
    scene: str
    factory: PudinkClientFactory
    scene_manager: SceneManager

    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        scene: str,
    ) -> None:
        self.factory = factory
        self.scene_manager = scene_manager
        self.scene = scene

    def switch_screen(self, scene: str) -> None:
        self.factory.set_scene(scene)
        self.scene_manager.switch_to_scene(scene)

    def send_message(self, data: Any) -> None:
        if self.factory.client is not None:
            self.factory.client.send_message(data)
        else:
            print(f"Client not connected, cannot send message {data}")

    def register_callback(
        self,
        callback: ClientCallback,
        function: Callable[[str], None],
        scene: str,
    ):
        self.factory.registerCallback(callback, function, scene)
