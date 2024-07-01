from pudink.server.handler.handler import Handler
from pudink.server.handler.handlers.not_initialized_handler import NotInitializedHandler


class DisconnectedHandler(NotInitializedHandler):
    def __init__(self, connection):
        super().__init__(connection)
