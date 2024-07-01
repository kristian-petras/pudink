from pudink.common.translator import MessageTranslator
from pudink.server.handler.handlers.connected_handler import ConnectedHandler
from pudink.server.handler.handlers.disconnected_handler import DisconnectedHandler
from pudink.server.handler.handlers.not_initialized_handler import NotInitializedHandler
from pudink.server.protocol.connection_states import ConnectionState


class MessageDispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.handlers = {
            ConnectionState.NOT_INITIALIZED: NotInitializedHandler(self.connection),
            ConnectionState.CONNECTED: ConnectedHandler(self.connection),
            ConnectionState.DISCONNECTED: DisconnectedHandler(self.connection),
        }

    def dispatch_message(self, message):
        handler = self.handlers[self.connection.state]

        if type(message) == bytes:
            message = MessageTranslator.decode(message)

        handler.handle_message(message)
