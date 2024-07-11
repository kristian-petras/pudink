from __future__ import annotations

import typing

from pudink.common.translator import MessageTranslator
from pudink.server.handler.handler import BaseHandler
from pudink.server.handler.handlers.connected_handler import ConnectedHandler
from pudink.server.handler.handlers.disconnected_handler import DisconnectedHandler
from pudink.server.protocol.connection_states import ConnectionState

if typing.TYPE_CHECKING:
    from pudink.server.protocol.pudink_connection import PudinkConnection


class MessageDispatcher:
    connection: PudinkConnection
    handlers: dict[ConnectionState, BaseHandler]

    def __init__(self, connection) -> None:
        self.connection = connection
        self.handlers = {
            ConnectionState.DISCONNECTED: DisconnectedHandler(self.connection),
            ConnectionState.CONNECTED: ConnectedHandler(self.connection),
        }

    def dispatch_message(self, message):
        handler = self.handlers[self.connection.state]

        if isinstance(message, bytes):
            message = MessageTranslator.decode(message)

        handler.handle_message(message)
