import pyglet

from pudink.client.controller.world_controller import WorldController
from pudink.common.model import Player, PlayerDisconnect, PlayerUpdate
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

    def after_scene_switch(self, previous_scene):
        self.window.push_handlers(self.keys)
        players = self.world_controller.get_players()
        for player in players.values():
            if player.id not in self.players:
                self.on_player_join(player)
            else:
                update = PlayerUpdate(player.id, player.x, player.y)
                self.on_player_update(update)

    def move_player(self, dt) -> None:
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
