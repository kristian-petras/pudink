from enum import Enum

from twisted.internet import protocol, reactor


class PlayerState(Enum):
    NOT_INITALIZED = 0
    INITIALIZED = 1


class PudinkServer(protocol.Protocol):
    def __init__(self):
        self.state = PlayerState.NOT_INITALIZED
        self.name = None

    def connectionMade(self):
        print("A client connected!")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        if self.state == PlayerState.NOT_INITALIZED:
            self.name = data.decode()
            self.state = PlayerState.INITIALIZED
            print(f"Player {self.name} initialized")
            # send a message to all other clients
            for c in self.factory.clients:
                if c != self:
                    c.transport.write(f"{self.name} joined the chat".encode())
            return

        print("received", repr(data))
        for c in self.factory.clients:
            if c != self:
                c.transport.write(data)


if __name__ == "__main__":
    factory = protocol.ServerFactory()
    factory.protocol = PudinkServer
    factory.clients = []
    reactor.listenTCP(8000, factory)
    reactor.run()
