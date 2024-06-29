from typing import Callable, Optional
from pudink.client.controller.base_controller import BaseController
from pudink.client.model.world_state import WorldState
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.protocol.factory import ClientCallback, PudinkClientFactory


from pudink.common.model import Player, PlayerDisconnect, PlayerUpdate


class WorldController(BaseController):
    on_player_join_callback: Optional[Callable[[Player], None]] = None
    on_player_leave_callback: Optional[Callable[[PlayerDisconnect], None]] = None
    on_player_update_callback: Optional[Callable[[PlayerUpdate], None]] = None

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
        self.factory.registerCallback(
            ClientCallback.CONNECTION_FAILED, self._on_disconnect, self.scene
        )

        self.on_player_join_callback = None
        self.on_player_update_callback = None
        self.on_player_leave_callback = None

    def move_player(self, new_x: int, new_y: int) -> None:
        player = self.get_current_player()
        if player is None:
            print("No player found when trying to move")
            return
        update = PlayerUpdate(player.id, new_x, new_y)
        self.player_update(update)
        self.factory.client.send_message(update)

    def _on_update(self, message: any) -> None:
        if type(message) == PlayerDisconnect:
            self.player_leave(message)
        elif type(message) == Player:
            self.player_join(message)
        elif type(message) == PlayerUpdate:
            self.player_update(message)
        else:
            print(f"Received unexpected message: {message}")

    def get_current_player(self) -> Optional[Player]:
        return self.world_state.get_current_player()

    def player_join(self, new_player: Player) -> None:
        self.world_state.add_player(new_player)
        if self.on_player_join_callback:
            self.on_player_join_callback(new_player)

    def player_leave(self, disconnected_player: PlayerDisconnect) -> None:
        self.world_state.remove_player(disconnected_player)
        if self.on_player_leave_callback:
            self.on_player_leave_callback(disconnected_player)

    def player_update(self, update: PlayerUpdate) -> None:
        self.world_state.add_player(update)
        if self.on_player_update_callback:
            self.on_player_update_callback(update)

    def _on_disconnect(self, data) -> None:
        print(f"Disconnected from server with message: {data}")
        self.switch_screen("login")
