import asyncio

import pyglet

from pudink.client.frontend.login_scene import LoginScene
from pudink.client.frontend.main_scene import MainScene
from pudink.client.frontend.scene_manager import SceneManager


def main():
    window = pyglet.window.Window(800, 600, "Pudink")
    scene_manager = SceneManager(window)
    window.on_draw = scene_manager.on_draw
    window.on_key_press = scene_manager.on_key_press

    server = Server()

    login_scene = LoginScene(window, scene_manager)
    main_scene = MainScene(window, scene_manager)

    main_scene_processor = MainSceneProcessor(server, main_scene)

    scene_manager.register_scene("login", login_scene)
    scene_manager.register_scene("main", main_scene)

    scene_manager.switch_to_scene("login")

    pyglet.app.run()


if __name__ == "__main__":
    main()


class Server:
    def __init__(self):
        self.counter = 0

    def fetch(self):
        self.counter += 1
        return self.counter


class MainSceneProcessor:
    def __init__(self, server, scene):
        self.server = server
        self.scene = scene

    def process(self):
        return self.server.fetch()
