import pyglet

from pudink.client.controller.world_controller import WorldController


class WorldRenderer:
    def __init__(self, window: pyglet.window.Window, controller: WorldController):
        self.window = window
        self.world_controller = controller

        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            "Main Screen",
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        character = pyglet.resource.image("character.png")

        self.character = pyglet.sprite.Sprite(
            character, x=window.width // 2, y=window.height // 2, batch=self.batch
        )

    def on_draw(self):
        self.window.clear()
        state = self.world_controller.get_state()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        pass
