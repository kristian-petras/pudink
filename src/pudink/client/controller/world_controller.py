from typing import Callable
from pudink.client.controller.base_controller import BaseController
from pudink.client.model.world_state import WorldState
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory

import json


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

        self.on_player_join_callback = None
        self.on_player_update_callback = None
        self.on_player_leave_callback = None

    def action(self, action):
        player = self.get_current_player()
        player.x = action["x"]
        player.y = action["y"]
        self.player_update(player)
        self.factory.client.send_message(player)

    def _on_update(self, data):
        message = json.loads(data)
        if message["type"] == "new_player":
            self.player_join(message["data"])
        elif message["type"] == "player_update":
            self.player_update(message["data"])
        elif message["type"] == "player_leave":
            self.player_leave(message["data"])

    def get_current_player(self):
        return self.world_state.get_current_player()

    def player_join(self, player):
        self.world_state.upsert_player(player)
        self.on_player_join_callback(player)

    def player_leave(self, player_id):
        self.world_state.remove_player(player_id)
        self.on_player_leave_callback(player_id)

    def player_update(self, player):
        self.world_state.upsert_player(player)
        self.on_player_update_callback(player)
