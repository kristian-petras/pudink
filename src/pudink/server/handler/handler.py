from pudink.common.model import (
    NewAccount,
    Credentials,
    PlayerUpdate,
    PlayerSnapshot,
    ChatMessage,
    PlayerDisconnect,
)
from pudink.common.translator import MessageTranslator


class Handler:
    def __init__(self, connection):
        self.connection = connection
        self.db = self.connection.db
        self.factory = self.connection.factory
        self.message_handlers = {
            NewAccount: self.handle_new_account,
            Credentials: self.handle_credentials,
            PlayerUpdate: self.handle_player_update,
            ChatMessage: self.handle_chat_message,
            PlayerDisconnect: self.handle_player_disconnect,
        }

    def handle_message(self, message):
        action = self.message_handlers[type(message)]
        if not action:
            raise NotImplemented(f"Unhandled message type: {type(message)}")

        action(message)

    def handle_new_account(self, message: NewAccount):
        raise NotImplemented()

    def handle_credentials(self, message: Credentials):
        raise NotImplemented()

    def handle_player_update(self, message: PlayerUpdate):
        raise NotImplemented()

    def handle_chat_message(self, message: ChatMessage):
        raise NotImplemented()

    def handle_player_disconnect(self, message: PlayerDisconnect):
        self.broadcast_message(message)

    def _send_error(self, error_message):
        error = MessageTranslator.encode(error_message)
        self.connection.transport.write(error)

    def _send_player_snapshot(self) -> None:
        player_snapshot = PlayerSnapshot(
            self.connection.player.id, self.factory.players.values()
        )
        player_snapshot = MessageTranslator.encode(player_snapshot)

        self.connection.transport.write(player_snapshot)

    def broadcast_new_player(self) -> None:
        self.broadcast_message(self.connection.player)

    def broadcast_message(self, message) -> None:
        if type(message) == bytes:
            message = MessageTranslator.decode(message)
        for c in self.factory.clients:
            if c != self.connection:
                c.transport.write(message)