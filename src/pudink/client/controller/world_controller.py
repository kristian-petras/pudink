from typing import Callable
from pudink.client.controller.base_controller import BaseController
from pudink.client.model.world_state import WorldState
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


class WorldController(BaseController):
    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        world_state: WorldState,
    ) -> None:
        super().__init__(factory, scene_manager)
        self.world_state = world_state

        self.factory.registerCallback(ClientCallback.DATA_RECEIVED, self._on_update)

    def get_state(self):
        return self.world_state

    def action(self, action):
        self.world_state.update(action)
        self.factory.client.send_message(action)

    def _on_update(self, data):
        self.world_state.update(data)
