import pyglet
from pyglet.gui import TextEntry
from pyglet.sprite import Sprite
from pyglet.window import Window, key

from pudink.client.controller.world_controller import WorldController
from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.renderer.base_renderer import BaseRenderer
from pudink.client.renderer.player_display import PlayerDisplay
from pudink.common.model import ChatMessage, Player, PlayerDisconnect, PlayerUpdate


class WorldRenderer(BaseRenderer):
    _players: dict[str, PlayerDisplay]
    _world_controller: WorldController

    _chat_entry: TextEntry
    _background_sprite: Sprite

    _keys: key.KeyStateHandler

    def __init__(
        self,
        window: Window,
        world_controller: WorldController,
        asset_manager: AssetManager,
    ) -> None:
        super().__init__(window, asset_manager)
        self._world_controller = world_controller

        self._world_controller.on_player_join_callback = self.on_player_join
        self._world_controller.on_player_leave_callback = self.on_player_leave
        self._world_controller.on_player_update_callback = self.on_player_update
        self._world_controller.on_chat_message_callback = self.on_chat_message

        self._chat_entry = self.create_entry(
            text="",
            x=20,
            y=20,
            handler=self._chat_handler,
        )

        self._players = {}
        self._keys = key.KeyStateHandler()

    def on_draw(self) -> None:
        super().on_draw()
        self.move_player(1 / 60)

    def _get_current_player(self) -> PlayerDisplay:
        player = self._world_controller.get_current_player()
        if player is None:
            raise ValueError("No current player found.")
        if player.id not in self._players:
            raise ValueError(f"Player with id {player.id} not found in player display.")
        return self._players[player.id]

    def _chat_handler(self, text: str) -> None:
        player = self._world_controller.get_current_player()
        if player is None:
            raise ValueError("No current player found.")
        chat_message = ChatMessage(player.id, text)
        self._world_controller.send_chat_message(text)
        self.on_chat_message(chat_message)
        self._chat_entry.value = ""

    def after_scene_switch(self) -> None:
        super().after_scene_switch()
        self.window.push_handlers(self._keys)
        players = self._world_controller.get_players()
        for player in players.values():
            if player.id not in self._players:
                self.on_player_join(player)
            else:
                update = PlayerUpdate(player.id, player.x, player.y)
                self.on_player_update(update)

    def move_player(self, dt: float) -> None:
        if self._chat_entry.focus:
            return

        movement_speed = 300 * dt
        # Calculate the movement in each direction
        dx = dy = 0.0
        if self._keys[pyglet.window.key.W]:
            dy += movement_speed
        if self._keys[pyglet.window.key.S]:
            dy -= movement_speed
        if self._keys[pyglet.window.key.A]:
            dx -= movement_speed
        if self._keys[pyglet.window.key.D]:
            dx += movement_speed

        # If there is no movement, do nothing
        if (dx, dy) == (0, 0):
            return

        current_player = self._world_controller.get_current_player()
        if current_player is None:
            return
        if current_player.id not in self._players:
            self.on_player_join(current_player)
            return

        # Normalize the movement vector
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length

        # Move the character
        change_x = dx * movement_speed
        change_y = dy * movement_speed

        new_x = round(current_player.x + change_x)
        new_y = round(current_player.y + change_y)

        # Update the frontend
        self._get_current_player().move(new_x, new_y)
        # Update the backend
        self._world_controller.move_player(new_x, new_y)

    def on_player_join(self, player: Player) -> None:
        print(f"Player {player.id} joined.")
        self._players[player.id] = PlayerDisplay(
            player.x,
            player.y,
            self.asset_manager.get_head(player.character.head_type),
            self.asset_manager.get_body(player.character.body_type),
            self.batch,
            self.foreground_group,
        )

    def on_player_leave(self, disconnect: PlayerDisconnect) -> None:
        print(f"Player with id {disconnect.id} disconnected.")
        self._players.pop(disconnect.id)

    def on_player_update(self, player: PlayerUpdate) -> None:
        self._players[player.id].move(player.x, player.y)

    def on_chat_message(self, chat_message: ChatMessage) -> None:
        player = self._players[chat_message.player_id]
        player.create_chat_bubble(chat_message.message)
        pyglet.clock.schedule_once(player.pop_chat_bubble, 5)
