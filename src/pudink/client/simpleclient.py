import pyglet
from twisted.internet import reactor, endpoints
from twisted.internet.task import LoopingCall
from twisted.internet.defer import Deferred
from twisted.internet.error import ReactorNotRunning

from pyglet.window import Window

from pudink.client.protocol.factory import PudinkClientFactory

background = pyglet.image.load("swamp.png")


class PudinkInfrastructure:
    def __init__(
        self,
        factory: PudinkClientFactory = PudinkClientFactory(),
        window: Window = Window(),
    ):
        self.factory = factory

        self.game_loop = LoopingCall(self._game_tick)
        self.game_loop_job = None

        self.window = window
        self.window.on_draw = lambda: background.blit(0, 0)
        self.window.on_close = self.stop
        self.window.on_key_press = lambda symbol, modifiers: print(symbol, modifiers)

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


# this connects the protocol to a server running on port 8000
def main():
    # Get reactor instance
    # # Create a player object
    # player = Player()

    # # Load the song file
    # song = pyglet.media.load("pesnicka.mp3")

    # # Queue the song for playback
    # player.queue(song)

    # # Start playing the song
    # player.play()
    game = PudinkInfrastructure()
    game.run()
    print("Game finished")


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
