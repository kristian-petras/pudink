import pyglet
from twisted.internet import reactor, endpoints
from twisted.internet.task import LoopingCall
from twisted.internet.error import ReactorNotRunning

from pyglet.window import Window

from pudink.client.protocol.factory import PudinkClientFactory
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.frontend.login_scene import LoginScene
from pudink.client.frontend.main_scene import MainScene


class PudinkGame:
    def __init__(
        self,
        factory: PudinkClientFactory = PudinkClientFactory(),
        window: Window = Window(800, 600, "Pudink"),
    ):
        self.factory = factory

        self.game_loop = LoopingCall(self._game_tick)
        self.game_loop_job = None

        self.window = window

        self.scene_manager = SceneManager(self.window)

        self.window.on_draw = self.scene_manager.on_draw
        self.window.on_key_press = self.scene_manager.on_key_press
        self.window.on_close = self.stop

        login_scene = LoginScene(self.window, self.scene_manager)
        main_scene = MainScene(self.window, self.scene_manager)

        self.scene_manager.register_scene("login", login_scene)
        self.scene_manager.register_scene("main", main_scene)

        self.scene_manager.switch_to_scene("login")

    def _game_tick(self):
        pyglet.clock.tick()
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()

    def run(self):
        self.game_loop_job = self.game_loop.start(1.0 / 30.0)
        endpoints.serverFromString(reactor, "tcp:8000").listen(self.factory)
        reactor.run()

    def stop(self):
        self.game_loop.stop()
        self.game_loop_job.addCallback(lambda _: self.window.close())
        try:
            reactor.stop()
        except ReactorNotRunning:
            print("Reactor already stopped")
            pass
