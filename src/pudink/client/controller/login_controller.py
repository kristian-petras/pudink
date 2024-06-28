from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


from typing import Callable


class LoginController:
    def __init__(self, factory: PudinkClientFactory, scene_manager) -> None:
        self.factory = factory
        self.scene_manager = scene_manager

    def login(
        self,
        input_data: dict[str, str],
        on_connecting: Callable[[str], None],
        on_success: Callable[[str], None],
        on_fail: Callable[[str], None],
    ) -> None:
        self.factory.registerCallback(ClientCallback.STARTED_CONNECTING, on_connecting)
        self.factory.registerCallback(ClientCallback.CONNECTION_FAILED, on_fail)
        self.factory.registerCallback(
            ClientCallback.CONNECTION_SUCCESS,
            lambda data: self._on_success(on_success, input_data, data),
        )
        self.factory.registerCallback(
            ClientCallback.DATA_RECEIVED, self._on_initialization
        )
        self.factory.connect()

    def switch_screen(self, scene):
        self.factory.set_scene(scene)
        self.scene_manager.switch_to_scene(scene)

    def _on_success(
        self,
        renderer_on_success: Callable[[str], None],
        input_data: dict[str, str],
        data: str,
    ):
        self.factory.client.send_message(input_data)
        renderer_on_success(data)

    def _on_initialization(self, data):
        print(data)
        print("initialized")
        self.switch_screen("main")
