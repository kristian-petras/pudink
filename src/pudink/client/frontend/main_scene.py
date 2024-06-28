import pyglet


class MainScene:
    def __init__(self, window, scene_manager):
        self.window = window
        self.scene_manager = scene_manager
        self.label = pyglet.text.Label(
            "Main Screen",
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
        )

    def on_draw(self):
        self.window.clear()
        self.label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.scene_manager.switch_to_scene("login")
