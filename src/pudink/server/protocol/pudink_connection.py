from twisted.internet import protocol

from pudink.common.model import PlayerDisconnect
from pudink.server.database.connector import GameDatabase
from pudink.server.handler.dispatcher import MessageDispatcher
from pudink.server.protocol.connection_states import ConnectionState


class PudinkConnection(protocol.Protocol):

    def __init__(self, db: GameDatabase, factory):
        self.factory = factory
        self.db = db
        self.player = None
        self.message_dispatcher = MessageDispatcher(self)
        self.state = ConnectionState.NOT_INITIALIZED

    def connectionMade(self):
        print("A client connected!")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.clients.remove(self)

        if self.state.CONNECTED and self.player:
            self.message_dispatcher.dispatch_message(PlayerDisconnect(self.player.id))

        self.state = ConnectionState.DISCONNECTED

    def dataReceived(self, data):
        self.message_dispatcher.dispatch_message(data)
