import pyglet

from pudink.client.frontend.login_scene import LoginScene
from pudink.client.frontend.main_scene import MainScene
from pudink.client.frontend.scene_manager import SceneManager


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_manager = SceneManager(self)
        login_scene = LoginScene(self)
        main_scene = MainScene(self)
        self.scene_manager.register_scene("login", login_scene)
        self.scene_manager.register_scene("main", main_scene)
        self.scene_manager.switch_to_scene("login")

    def on_draw(self):
        self.scene_manager.on_draw()

    def on_key_press(self, symbol, modifiers):
        self.scene_manager.on_key_press(symbol, modifiers)
