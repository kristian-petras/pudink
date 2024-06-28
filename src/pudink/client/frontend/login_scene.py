import pyglet

from pudink.client.protocol.factory import PudinkClientFactory


class LoginScene:
    def __init__(self, window, scene_manager, connect, factory: PudinkClientFactory):
        self.window = window
        self.scene_manager = scene_manager
        self.label = pyglet.text.Label(
            "Login Screen",
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
        )
        self.connect = connect
        self.factory = factory

        self.factory.registeredCallbacks.append(self.test)

    def on_draw(self):
        self.window.clear()
        self.label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.scene_manager.switch_to_scene("main")
            # self.factory.client.transport.write(b"Hello, world!")
        elif symbol == pyglet.window.key.ESCAPE:
            self.connect()

    def test(self):
        print("Test")
