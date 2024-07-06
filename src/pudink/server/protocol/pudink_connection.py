from __future__ import annotations

import typing

from twisted.internet import protocol
from twisted.internet.interfaces import ITransport
from twisted.python.failure import Failure

from pudink.common.model import Player, PlayerDisconnect
from pudink.server.database.connector import GameDatabase
from pudink.server.handler.dispatcher import MessageDispatcher
from pudink.server.protocol.connection_states import ConnectionState

if typing.TYPE_CHECKING:
    from pudink.server.protocol.pudink_server import PudinkServer


class PudinkConnection(protocol.Protocol):
    factory: PudinkServer
    db: GameDatabase
    player: Player | None
    message_dispatcher: MessageDispatcher
    state: ConnectionState
    transport: ITransport

    def __init__(self, db: GameDatabase, factory: PudinkServer) -> None:
        self.factory = factory
        self.db = db
        self.player = None
        self.message_dispatcher = MessageDispatcher(self)
        self.state = ConnectionState.DISCONNECTED

    def connectionMade(self) -> None:
        print("A client connected!")
        self.factory.clients.append(self)

    def connectionLost(self, reason: Failure) -> None:
        print("Lost a client!")
        self.factory.clients.remove(self)

        if self.state.CONNECTED and self.player:
            self.message_dispatcher.dispatch_message(PlayerDisconnect(self.player.id))

        self.state = ConnectionState.DISCONNECTED

    def dataReceived(self, data: bytes) -> None:
        self.message_dispatcher.dispatch_message(data)
