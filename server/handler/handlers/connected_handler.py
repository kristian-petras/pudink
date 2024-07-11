from common.model import ChatMessage, PlayerUpdate
from server.handler.handler import BaseHandler


class ConnectedHandler(BaseHandler):
    def __init__(self, connection):
        super().__init__(connection)

    def handle_chat_message(self, message: ChatMessage) -> None:
        self.broadcast_message(message)

    def handle_player_update(self, message: PlayerUpdate) -> None:
        if self.connection.player is None:
            print("Player not initialized")
            return
        self.connection.player.x = message.x
        self.connection.player.y = message.y
        self.broadcast_message(message)
