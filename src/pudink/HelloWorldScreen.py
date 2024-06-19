import pyglet


class HelloWorldScreen:
    def __init__(self, game):
        self.window = game

        self.label = pyglet.text.Label(
            "Hello World",
            font_size=36,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x="center",
            anchor_y="center",
        )

    def on_draw(self):
        self.window.clear()
        self.label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        print("aoao")
