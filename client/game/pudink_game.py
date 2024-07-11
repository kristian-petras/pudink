from typing import Optional

import pyglet
from pyglet.window import Window
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.error import ReactorNotRunning
from twisted.internet.task import LoopingCall

from pudink.client.controller.menu_controller import MenuController
from pudink.client.controller.title_controller import TitleController
from pudink.client.controller.world_controller import WorldController
from pudink.client.frontend.asset_manager import AssetManager
from pudink.client.frontend.scene_manager import SceneManager
from pudink.client.game.client_factory import PudinkClientFactory
from pudink.client.game.world_state import WorldState
from pudink.client.renderer.menu_renderer import MenuRenderer
from pudink.client.renderer.title_renderer import TitleRenderer
from pudink.client.renderer.world_renderer import WorldRenderer


class PudinkGame:
    """
    Represents the main game class for Pudink. Initializes all game components and runs the game loop.

    Attributes:
        _factory (PudinkClientFactory): The client factory used for network communication.
        _host (str): The host address to connect to.
        _port (int): The port number to connect to.
        _game_loop (LoopingCall): The looping call for the game tick.
        _game_loop_job (Optional[Deferred[LoopingCall]]): The deferred job for the game loop.
        _window (Window): The Pyglet window for rendering the game.

    Args:
        window (Window): The Pyglet window for rendering the game.
        factory (PudinkClientFactory): The client factory used for network communication.
        host (str, optional): The host address to connect to. Defaults to "localhost".
        port (int, optional): The port number to connect to. Defaults to 8000.
    """

    _factory: PudinkClientFactory
    _host: str
    _port: int
    _game_loop: LoopingCall
    _game_loop_job: Optional[Deferred[LoopingCall]]
    _window: Window

    def __init__(
        self,
        window: Window,
        factory: PudinkClientFactory,
        host: str = "localhost",
        port: int = 8000,
    ):
        """
        Initializes a new instance of the PudinkGame class.

        Args:
            window (Window): The Pyglet window for rendering the game.
            factory (PudinkClientFactory): The client factory used for network communication.
            host (str, optional): The host address to connect to. Defaults to "localhost".
            port (int, optional): The port number to connect to. Defaults to 8000.
        """
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
        world_controller = WorldController(self._factory, scene_manager, world_state)
        world_scene = WorldRenderer(self._window, world_controller, asset_manager)
        title_controller = TitleController(self._factory, scene_manager)
        title_renderer = TitleRenderer(self._window, asset_manager, title_controller)
        menu_controller = MenuController(self._factory, scene_manager, world_state)
        menu_renderer = MenuRenderer(self._window, asset_manager, menu_controller)

        scene_manager.register_scene(title_controller.scene, title_renderer)
        scene_manager.register_scene(menu_controller.scene, menu_renderer)
        scene_manager.register_scene(world_controller.scene, world_scene)

        title_controller.switch_screen(title_controller.scene)
        print("Game started")

    def _game_tick(self):
        """
        Performs a single game tick.

        This method is called by the game loop at a fixed interval.
        It updates the game state, handles user input, and renders the game.
        """
        pyglet.clock.tick()
        self._window.switch_to()
        self._window.dispatch_events()
        self._window.dispatch_event("on_draw")
        self._window.flip()

    def run(self):
        """
        Runs the game.

        This method starts the game loop and runs the Pyglet event loop.
        """
        self._game_loop_job = self._game_loop.start(1.0 / 30.0)
        reactor.run()  # type: ignore

    def stop(self):
        """
        Stops the game.

        This method stops the game loop, closes the window, and stops the reactor.
        """
        self._game_loop.stop()

        if self._game_loop_job:
            self._game_loop_job.addCallback(lambda _: self._window.close())
        else:
            self._window.close()
            print("Game already stopped")

        try:
            reactor.stop()  # type: ignore
        except ReactorNotRunning:
            print("Reactor already stopped")

    def _connect(self):
        """
        Connects to the server.

        This method establishes a TCP connection to the server using the specified host and port.
        """
        reactor.connectTCP(self._host, self._port, self._factory)  # type: ignore
