from pudink.common.model import (
    NewAccount,
    Credentials,
    ConnectionFailure,
    Player,
    PlayerInitialization,
)
from pudink.common.translator import MessageTranslator
from pudink.server.handler.handler import Handler
from pudink.server.protocol.connection_states import ConnectionState


class DisconnectedHandler(Handler):
    def __init__(self, connection):
        super().__init__(connection)

    def handle_new_account(self, message: NewAccount):
        if len(message.name) < 3 or len(message.password) < 3:
            fail = ConnectionFailure(
                "Name and password must be at least 3 characters long"
            )
            self._send_error(fail)
            return
        account = self.db.register_user(message)
        if self._is_successful(account):
            self.handle_credentials(Credentials(message.name, message.password))
        else:
            self._send_error(account)

    def handle_credentials(self, message: Credentials):
        print("Authenticating player with credentials: ", message)

        player = self.db.authenticate_user(message)

        if not self._is_successful(player):
            self._send_error(player)
            return

        if self._is_player_connected(player):
            self._send_error(ConnectionFailure("Player already connected!"))
            return

        if self._is_player_instance_missing(player):
            print(f"Creating new player {player.id}")
            self.connection.player = Player(player.id, player.character, 400, 400)
            self.factory.players[self.connection.player.id] = self.connection.player

        print(f"Player with id {player.id} initialized")

        self._send_player_snapshot()
        self.broadcast_new_player()
        self.connection.state = ConnectionState.CONNECTED

    def _is_player_connected(self, player):
        connected_players = [
            client.player.id
            for client in self.connection.factory.clients
            if client.state == ConnectionState.CONNECTED
        ]
        return player.id in connected_players

    def _is_player_instance_missing(self, player):
        return (
            player.id not in self.connection.factory.players
            or self.connection.player is None
        )

    def _is_successful(self, player):
        return not isinstance(player, ConnectionFailure)
