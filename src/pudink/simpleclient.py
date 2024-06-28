# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

import random
import string
import time

import pyglet
from pyglet.media import Player
from twisted.internet import protocol, reactor
from twisted.internet.task import LoopingCall
from twisted.internet.defer import Deferred

background = pyglet.image.load("swamp.png")


class Test:
    def __init__(self, factory, window):
        self.factory = factory
        self.window = window

    def game_tick(self):
        pyglet.clock.tick()
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()

        # print("tick")
        # if factory.client:
        #     print("sending tick")
        #     factory.client.sendMessage("tick")


class EchoClient(protocol.Protocol):
    def generate_random_name(self):
        length = random.randint(5, 10)
        name = "".join(random.choices(string.ascii_lowercase, k=length))
        return name

    def connectionMade(self):
        random_name = self.generate_random_name()
        self.transport.write(random_name.encode())

    def dataReceived(self, data):
        print("Server said:", data)

    def connectionLost(self, reason):
        print("connection lost")

    def sendMessage(self, msg):
        self.transport.write(msg.encode())


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.client = None

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

    def buildProtocol(self, addr):
        p = EchoClient()
        p.factory = self
        self.client = p
        return p


def stop(window: pyglet.window.Window, event: LoopingCall, a: Deferred[LoopingCall]):
    # reactor.stop()
    event.stop()
    a.addCallback(lambda _: window.close())


# this connects the protocol to a server running on port 8000
def main():
    factory = EchoFactory()
    window = pyglet.window.Window()
    # Create a player object
    player = Player()

    # Load the song file
    song = pyglet.media.load("pesnicka.mp3")

    # Queue the song for playback
    player.queue(song)

    # Start playing the song
    player.play()

    t = Test(factory, window)
    tick = LoopingCall(t.game_tick)
    a = tick.start(1.0 / 30.0)

    window.on_draw = lambda: background.blit(0, 0)
    window.on_close = lambda: stop(window, tick, a)

    reactor.connectTCP("localhost", 8000, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
