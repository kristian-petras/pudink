from pudink.common.model import NewAccount, Credentials, PlayerUpdate, ChatMessage
from pudink.server.handler.handler import Handler


class ConnectedHandler(Handler):
    def __init__(self, connection):
        super().__init__(connection)

    def handle_chat_message(self, message: ChatMessage):
        self.broadcast_message(message)

    def handle_player_update(self, message: PlayerUpdate):
        self.connection.player.x = message.x
        self.connection.player.y = message.y
        self.broadcast_message(message)
