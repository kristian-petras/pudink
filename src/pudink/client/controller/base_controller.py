from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


from typing import Callable


class BaseController:
    def __init__(self, factory: PudinkClientFactory, scene_manager) -> None:
        self.factory = factory
        self.scene_manager = scene_manager

    def switch_screen(self, scene):
        self.factory.set_scene(scene)
        self.scene_manager.switch_to_scene(scene)

    def send_message(self, input_data: dict[str, str]):
        self.factory.client.send_message(input_data)

    def register_callback(
        self, callback: ClientCallback, function: Callable[[str], None]
    ):
        self.factory.registerCallback(callback, function)
