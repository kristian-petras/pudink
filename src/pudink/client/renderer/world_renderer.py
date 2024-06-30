import pyglet

from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.controller.world_controller import WorldController
from pudink.client.frontend.color_palette import ColorPalette
from pudink.client.renderer.player_display import PlayerDisplay
from pudink.common.model import ChatMessage, Player, PlayerDisconnect, PlayerUpdate
from pyglet.window import Window, key


class WorldRenderer:
    players: dict[int, PlayerDisplay]

    def __init__(
        self,
        window: Window,
        world_controller: WorldController,
        asset_manager: AssetManager,
    ) -> None:
        self.window = window
        self.world_controller = world_controller
        self.batch = pyglet.graphics.Batch()
        self.asset_manager = asset_manager

        self.world_controller.on_player_join_callback = self.on_player_join
        self.world_controller.on_player_leave_callback = self.on_player_leave
        self.world_controller.on_player_update_callback = self.on_player_update
        self.world_controller.on_chat_message_callback = self.on_chat_message

        self.background_group = pyglet.graphics.Group(0)
        self.foreground_group = pyglet.graphics.Group(1)

        self.chat_entry = pyglet.gui.TextEntry(
            "",
            20,
            20,
            200,
            batch=self.batch,
            group=self.foreground_group,
            color=ColorPalette.LIGHT.value,
            text_color=ColorPalette.DARK.value,
            caret_color=ColorPalette.DARK.value,
        )
        self.chat_entry.set_handler("on_commit", self._chat_handler)

        self.background = asset_manager.get_background()
        self.background_sprite = pyglet.sprite.Sprite(
            self.background, x=0, y=0, batch=self.batch, group=self.background_group
        )

        self.players = {}
        self.keys = key.KeyStateHandler()

    def on_draw(self) -> None:
        self.window.clear()
        self.batch.draw()
        self.move_player(1 / 60)

    def on_key_press(self, symbol, modifiers):
        pass

    def before_scene_switch(self):
        self.window.remove_handlers()

    def _get_current_player(self):
        id = self.world_controller.get_current_player().id
        if id not in self.players:
            raise ValueError(f"Player with id {id} not found.")
        return self.players[id]

    def _chat_handler(self, text):
        self.world_controller.send_chat_message(text)
        chat_message = ChatMessage(self.world_controller.get_current_player().id, text)
        self.on_chat_message(chat_message)
        self.chat_entry.value = ""

    def after_scene_switch(self, previous_scene):
        self.window.push_handlers(self.chat_entry)
        self.window.push_handlers(self.keys)
        players = self.world_controller.get_players()
        for player in players.values():
            if player.id not in self.players:
                self.on_player_join(player)
            else:
                update = PlayerUpdate(player.id, player.x, player.y)
                self.on_player_update(update)

    def move_player(self, dt) -> None:
        if self.chat_entry.focus:
            return

        movement_speed = 200 * dt
        # Calculate the movement in each direction
        dx = dy = 0
        if self.keys[pyglet.window.key.W]:
            dy += movement_speed
        if self.keys[pyglet.window.key.S]:
            dy -= movement_speed
        if self.keys[pyglet.window.key.A]:
            dx -= movement_speed
        if self.keys[pyglet.window.key.D]:
            dx += movement_speed

        # If there is no movement, do nothing
        if (dx, dy) == (0, 0):
            return

        current_player = self.world_controller.get_current_player()
        if current_player is None:
            return
        if current_player.id not in self.players:
            self.on_player_join(current_player)
            return

        # Normalize the movement vector
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length

        # Move the character
        new_x = current_player.x + dx * movement_speed
        new_y = current_player.y + dy * movement_speed

        # Update the frontend
        self._get_current_player().move(new_x, new_y)
        # Update the backend
        self.world_controller.move_player(new_x, new_y)

    def on_player_join(self, player: Player):
        print(f"Player {player.id} joined.")
        self.players[player.id] = PlayerDisplay(
            player.x,
            player.y,
            self.asset_manager.get_head(player.character.head_type),
            self.asset_manager.get_body(player.character.body_type),
            self.batch,
            self.foreground_group,
        )

    def on_player_leave(self, disconnect: PlayerDisconnect):
        print(f"Player with id {disconnect.id} disconnected.")
        self.players.pop(disconnect.id)

    def on_player_update(self, player: PlayerUpdate):
        self.players[player.id].move(player.x, player.y)

    def on_chat_message(self, chat_message: ChatMessage):
        player = self.players[chat_message.player_id]
        player.create_chat_bubble(chat_message.message)
        pyglet.clock.schedule_once(player.pop_chat_bubble, 5)
