from typing import Any, Callable

from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.game.client import ClientCallback
from pudink.client.game.client_factory import PudinkClientFactory


class BaseController:
    """
    The base controller class for managing scenes and sending messages to the client.
    """

    scene: str
    _factory: PudinkClientFactory
    _scene_manager: SceneManager

    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        scene: str,
    ) -> None:
        """
        Initializes a new instance of the BaseController class.

        Args:
            factory (PudinkClientFactory): The factory used to create the Pudink client.
            scene_manager (SceneManager): The scene manager used to manage scenes.
            scene (str): The name of the scene associated with the controller.
        """
        self._factory = factory
        self._scene_manager = scene_manager
        self.scene = scene

    def switch_screen(self, scene: str) -> None:
        """
        Switches the screen to the specified scene.
        Requires the scene to be registered beforehand.

        Args:
            scene (str): The name of the scene to switch to.

        Returns:
            None
        """
        self._factory.set_scene(scene)
        self._scene_manager.switch_to_scene(scene)

    def send_message(self, data: Any) -> None:
        """
        Sends a message to the client.

        Args:
            data (Any): The data to be sent.

        Returns:
            None
        """
        if self._factory.client is not None:
            self._factory.client.send_message(data)
        else:
            print(f"Client not connected, cannot send message {data}")

    def register_callback(
        self,
        callback: ClientCallback,
        function: Callable[[Any], None],
        scene: str,
    ) -> None:
        """
        Register a callback function for a specific scene.

        Args:
            callback (ClientCallback): The callback type.
            function (Callable[[Any], None]): The callback function to be registered.
            scene (str): The scene for which the callback is registered.

        Returns:
            None
        """
        self._factory.register_callback(callback, function, scene)
