import pyglet

from pudink.client.controller.world_controller import WorldController
from pudink.common.model import ChatMessage, Player, PlayerDisconnect, PlayerUpdate
from pyglet.window import Window, key


class WorldRenderer:
    def __init__(self, window: Window, world_controller: WorldController) -> None:
        self.window = window
        self.world_controller = world_controller
        self.batch = pyglet.graphics.Batch()

        self.character_image = pyglet.resource.image("character.png")

        self.world_controller.on_player_join_callback = self.on_player_join
        self.world_controller.on_player_leave_callback = self.on_player_leave
        self.world_controller.on_player_update_callback = self.on_player_update
        self.world_controller.on_chat_message_callback = self.on_chat_message

        self.chat_entry = pyglet.gui.TextEntry("", 20, 20, 200, batch=self.batch)
        self.chat_entry.set_handler("on_commit", self._chat_handler)

        self.players = {}
        self.chat_bubbles = {}
        self.keys = key.KeyStateHandler()

    def on_draw(self) -> None:
        self.window.clear()
        self.batch.draw()
        self.move_player(1 / 60)

    def on_key_press(self, symbol, modifiers):
        pass

    def before_scene_switch(self):
        self.window.remove_handlers()

    def _chat_handler(self, text):
        self.world_controller.send_chat_message(text)
        player = self.world_controller.get_current_player()
        self._register_chat_bubble(player, text)
        self.chat_entry.value = ""

    def pop_chat_bubble(self, player_id):
        if player_id in self.chat_bubbles:
            self.chat_bubbles[player_id].pop(0).delete()
            player = self.players[player_id]
            self._move_chat_bubbles(player_id, player.x, player.y)

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

        current_player = self.world_controller.get_current_player()
        if current_player is None:
            return
        if current_player.id not in self.players:
            self.on_player_join(current_player)
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

        # Normalize the movement vector
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length

        # Move the character
        active_player = self.players[current_player.id]
        active_player.x += dx * movement_speed
        active_player.y += dy * movement_speed

        # Update the chat bubbles
        self._move_chat_bubbles(current_player.id, active_player.x, active_player.y)

        # Update the player's location
        self.world_controller.move_player(active_player.x, active_player.y)

    def on_player_join(self, player: Player):
        print(f"Player {player.id} joined.")
        self.players[player.id] = pyglet.sprite.Sprite(
            self.character_image,
            x=player.x,
            y=player.y,
            batch=self.batch,
        )

    def on_player_leave(self, disconnect: PlayerDisconnect):
        print(f"Player with id {disconnect.id} disconnected.")
        self.players.pop(disconnect.id)

    def on_player_update(self, player: PlayerUpdate):
        self.players[player.id].x = player.x
        self.players[player.id].y = player.y
        self._move_chat_bubbles(player.id, player.x, player.y)

    def on_chat_message(self, chat_message: ChatMessage):
        player = self.world_controller.get_player(chat_message.player_id)
        self._register_chat_bubble(player, chat_message.message)

    def _register_chat_bubble(self, player: Player, message: str):
        if player.id not in self.chat_bubbles:
            self.chat_bubbles[player.id] = []

        chat_bubbles = self.chat_bubbles[player.id]
        label = pyglet.text.Label(
            message,
            x=player.x,
            y=player.y + 50 + 20 * len(chat_bubbles),
            batch=self.batch,
            color=(0, 0, 0, 255),
        )

        self.chat_bubbles[player.id].append(label)
        # Remove the chat bubble after 5 seconds
        pyglet.clock.schedule_once(lambda _: self.pop_chat_bubble(player.id), 5)

    def _move_chat_bubbles(self, player_id, x, y):
        if player_id in self.chat_bubbles:
            for index, bubble in enumerate(self.chat_bubbles[player_id]):
                bubble.x = x
                bubble.y = y + 50 + 20 * index
