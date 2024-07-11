from __future__ import annotations

import typing

from pudink.common.model import (
    ConnectionFailure,
    Credentials,
    NewAccount,
    Player,
    PlayerInitialization,
)
from pudink.server.handler.handler import BaseHandler
from pudink.server.protocol.connection_states import ConnectionState

if typing.TYPE_CHECKING:
    from pudink.server.protocol.pudink_connection import PudinkConnection


class DisconnectedHandler(BaseHandler):
    def __init__(self, connection: PudinkConnection):
        super().__init__(connection)

    def handle_new_account(self, message: NewAccount) -> None:
        if len(message.name) < 3 or len(message.password) < 3:
            self._send_error(
                ConnectionFailure(
                    "Name and password must be at least 3 characters long"
                )
            )
            return
        account = self.db.register_user(message)
        if isinstance(account, PlayerInitialization):
            self.handle_credentials(Credentials(message.name, message.password))
        elif isinstance(account, ConnectionFailure):
            self._send_error(account)
        else:
            self._send_error(
                ConnectionFailure(f"Invalid account creation, received: {account}")
            )

    def handle_credentials(self, message: Credentials) -> None:
        print("Authenticating player with credentials: ", message)

        player = self.db.authenticate_user(message)

        if isinstance(player, ConnectionFailure):
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

    def _is_player_connected(self, player) -> bool:
        connected_players = [
            client.player.id
            for client in self.connection.factory.clients
            if client.state == ConnectionState.CONNECTED and client.player
        ]
        return player.id in connected_players

    def _is_player_instance_missing(self, player) -> bool:
        return (
            player.id not in self.connection.factory.players
            or self.connection.player is None
        )
