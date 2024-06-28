from typing import Callable, Optional
from pudink.client.controller.base_controller import BaseController
from pudink.client.model.player import Player
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
        self.scene = "world"
        self.factory.registerCallback(
            ClientCallback.DATA_RECEIVED, self._on_update, self.scene
        )

        self.on_player_join_callback = None
        self.on_player_update_callback = None
        self.on_player_leave_callback = None

    def action(self, action):
        print("performing action")
        player = self.get_current_player()
        player.location = (action["data"]["x"], action["data"]["y"])
        self.player_update(player)
        self.factory.client.send_message(action)
        print(f"performing action finished, sent {action} to server")

    def _on_update(self, data):
        print("hoogg")
        message = json.loads(data)
        print(f"received update {message}")
        if message["type"] == "new_player":
            self.player_join(message["data"])
        elif message["type"] == "player_update":
            player = Player(
                message["data"]["id"],
                message["data"]["username"],
                (message["data"]["x"], message["data"]["y"]),
            )
            self.player_update(player)
        elif message["type"] == "player_leave":
            self.player_leave(message["data"])

    def get_current_player(self) -> Optional[Player]:
        return self.world_state.get_current_player()

    def player_join(self, player):
        p = Player(player["id"], player["username"], (player["x"], player["y"]))
        self.world_state.upsert_player(p)
        if self.on_player_join_callback:
            self.on_player_join_callback(p)
        else:
            print("no on_player_join_callback")

    def player_leave(self, player_id):
        self.world_state.remove_player(player_id)
        if self.on_player_leave_callback:
            self.on_player_leave_callback(player_id)

    def player_update(self, player):
        print("player_update")
        self.world_state.upsert_player(player)
        if self.on_player_update_callback:
            self.on_player_update_callback(player)
        print("player_update finished")
