import pyglet
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.error import ReactorNotRunning

from pyglet.window import Window

from pudink.client.controller.login_controller import LoginController
from pudink.client.protocol.factory import PudinkClientFactory
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.renderer.login_renderer import LoginRenderer
from pudink.client.frontend.main_scene import MainScene


class PudinkGame:
    def __init__(
        self,
        window: Window,
        factory: PudinkClientFactory,
        host: str = "localhost",
        port: int = 8000,
    ):
        self._factory = factory
        self._host = host
        self._port = port

        self._game_loop = LoopingCall(self._game_tick)
        self._game_loop_job = None

        self._window = window

        self._scene_manager = SceneManager(self._window)

        self._window.on_draw = self._scene_manager.on_draw
        self._window.on_key_press = self._scene_manager.on_key_press
        self._window.on_close = self.stop

        login_controller = LoginController(self._factory, self._scene_manager)
        login_scene = LoginRenderer(self._window, login_controller)
        main_scene = MainScene(self._window, self._scene_manager)

        self._scene_manager.register_scene("login", login_scene)
        self._scene_manager.register_scene("main", main_scene)

        login_controller.switch_screen("login")

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
