import pyglet
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.error import ReactorNotRunning

from pyglet.window import Window

from pudink.client.asset_mapping import AssetManager
from pudink.client.controller.login_controller import LoginController
from pudink.client.controller.world_controller import WorldController
from pudink.client.model.world_state import WorldState
from pudink.client.protocol.factory import PudinkClientFactory
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.renderer.login_renderer import LoginRenderer
from pudink.client.renderer.world_renderer import WorldRenderer


class PudinkGame:
    def __init__(
        self,
        window: Window,
        factory: PudinkClientFactory,
        host: str = "localhost",
        port: int = 8000,
    ):
        print("Starting game")
        self._factory = factory
        self._host = host
        self._port = port

        self._game_loop = LoopingCall(self._game_tick)
        self._game_loop_job = None

        self._window = window

        scene_manager = SceneManager(self._window)

        self._window.on_draw = scene_manager.on_draw
        self._window.on_key_press = scene_manager.on_key_press
        self._window.on_close = self.stop

        pyglet.resource.path = ["assets", "assets/ui", "assets/head", "assets/body"]
        pyglet.resource.reindex()

        world_state = WorldState()
        asset_manager = AssetManager()
        login_controller = LoginController(self._factory, scene_manager, world_state)
        login_scene = LoginRenderer(self._window, login_controller, asset_manager)
        world_controller = WorldController(self._factory, scene_manager, world_state)
        world_scene = WorldRenderer(self._window, world_controller, asset_manager)

        scene_manager.register_scene("login", login_scene)
        scene_manager.register_scene("world", world_scene)

        login_controller.switch_screen("login")
        print("Game started")

    def _game_tick(self):
        pyglet.clock.tick()
        self._window.switch_to()
        self._window.dispatch_events()
        self._window.dispatch_event("on_draw")
        self._window.flip()

    def run(self):
        self._game_loop_job = self._game_loop.start(1.0 / 30.0)
        reactor.run()

    def stop(self):
        self._game_loop.stop()
        self._game_loop_job.addCallback(lambda _: self._window.close())
        try:
            reactor.stop()
        except ReactorNotRunning:
            print("Reactor already stopped")
            pass

    def _connect(self):
        reactor.connectTCP(self._host, self._port, self._factory)
