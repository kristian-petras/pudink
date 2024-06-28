from enum import Enum

from twisted.internet import protocol, reactor
import json


class PlayerState(Enum):
    NOT_INITALIZED = 0
    INITIALIZED = 1


class PudinkServer(protocol.Protocol):
    def __init__(self):
        self.state = PlayerState.NOT_INITALIZED
        self.username = None
        self.password = None
        self.id = None

        self.x = 400
        self.y = 400

    def connectionMade(self):
        print("A client connected!")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        player_leave_message = {"type": "player_leave", "data": self.id}
        self.factory.clients.remove(self)
        for c in self.factory.clients:
            c.transport.write(json.dumps(player_leave_message).encode())

    def dataReceived(self, data):
        if self.state == PlayerState.NOT_INITALIZED:
            account_info = json.loads(data.decode())
            self.username = account_info["username"]
            self.password = account_info["password"]
            self.state = PlayerState.INITIALIZED

            self.id = self.factory.id
            self.factory.id += 1

            print(f"Player {self.username} initialized with id {self.id}")

            snapshot = {
                "current_player_id": self.id,
                "players": [
                    {"id": c.id, "username": c.username, "x": c.x, "y": c.y}
                    for c in self.factory.clients
                ],
            }

            print(f"sending info about other players to the new player {snapshot}")
            self.transport.write(json.dumps(snapshot).encode())

            new_player_message = {
                "type": "new_player",
                "data": {
                    "id": self.id,
                    "username": self.username,
                    "x": self.x,
                    "y": self.y,
                },
            }
            for c in self.factory.clients:
                if c != self:
                    c.transport.write(json.dumps(new_player_message).encode())
            return

        print("received", repr(data))
        for c in self.factory.clients:
            if c != self:
                print(f"sending to {c.id}")
                c.transport.write(data)


if __name__ == "__main__":
    factory = protocol.ServerFactory()
    factory.protocol = PudinkServer
    factory.clients = []
    factory.players = {}
    factory.id = 0
    reactor.listenTCP(8000, factory)
    reactor.run()
