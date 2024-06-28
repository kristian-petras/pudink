import pyglet

from pudink.client.controller.world_controller import WorldController


class WorldRenderer:
    def __init__(self, window: pyglet.window.Window, world_controller: WorldController):
        self.window = window
        self.world_controller = world_controller

        self.batch = pyglet.graphics.Batch()

        self.character_image = pyglet.resource.image("character.png")

        self.world_controller.on_player_join_callback = self.on_player_join
        self.world_controller.on_player_leave_callback = self.on_player_leave
        self.world_controller.on_player_update_callback = self.on_player_update

        self.players = {}
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1 / 60)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        # Define the movement speed
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

        # Normalize the movement vector
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length

        # Move the character
        current_player = self.world_controller.get_current_player()
        current_player_sprite = self.players[current_player.id]
        current_player_sprite.x += dx * movement_speed
        current_player_sprite.y += dy * movement_speed

        self.world_controller.action(
            {"x": current_player_sprite.x, "y": current_player_sprite.y}
        )

    def on_player_join(self, player):
        self.players[player.id] = pyglet.sprite.Sprite(
            self.character_image,
            x=player.x,
            y=player.y,
            batch=self.batch,
        )

    def on_player_leave(self, player_id):
        self.players.pop(player_id)

    def on_player_update(self, player):
        self.players[player.id].x = player.x
        self.players[player.id].y = player.y
