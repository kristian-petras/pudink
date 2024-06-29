from enum import Enum
from typing import Optional
from twisted.internet import protocol, reactor
import os

from pudink.common.model import (
    ConnectionError,
    Player,
    PlayerDisconnect,
    PlayerInitialization,
    PlayerSnapshot,
)
from pudink.common.translator import MessageTranslator
from pudink.server.database.connector import GameDatabase


class PudinkConnection(protocol.Protocol):
    def __init__(self):
        self.player = None
        self.db_file = os.path.join(os.path.dirname(__file__), "./database/game.db")
        self.db = GameDatabase(self.db_file)

    def connectionMade(self):
        print("A client connected!")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        if self.player is None:
            return
        self.factory.clients.remove(self)
        del self.factory.players[self.player.id]
        self._broadcast_disconnect_player()
        self.player = None

    def dataReceived(self, data):
        if self.player is None:
            player = self._authenticate_player(data)

            if player is None:
                error = MessageTranslator.encode(ConnectionError("Wrong credentials!"))
                self.transport.write(error)
                return

            if player.id in self.factory.players:
                error = MessageTranslator.encode(
                    ConnectionError("Player already connected!")
                )
                self.transport.write(error)
                return

            print(f"Player with id {player.id} initialized")
            self.player = Player(player.id, player.character, 400, 400)

            if self.player.id not in self.factory.players:
                self.factory.players[self.player.id] = self.player

            self._send_player_snapshot()
            self._broadcast_new_player()
        else:
            update = MessageTranslator.decode(data)
            self.player.x = update.x
            self.player.y = update.y
            self._broadcast_message(data)

    def _authenticate_player(self, data) -> Optional[PlayerInitialization]:
        credentials = MessageTranslator.decode(data)

        player = self.db.authenticate_user(credentials.name, credentials.password)
        if not player:
            error = MessageTranslator.encode(ConnectionError("Wrong credentials!"))
            self.transport.write(error)
            return None
        return player

    def _send_player_snapshot(self) -> None:
        playerSnapshot = MessageTranslator.encode(
            PlayerSnapshot(self.player.id, self.factory.players.values())
        )
        self.transport.write(playerSnapshot)

    def _broadcast_new_player(self) -> None:
        new_player = MessageTranslator.encode(self.player)
        self._broadcast_message(new_player)

    def _broadcast_disconnect_player(self) -> None:
        disconnect = MessageTranslator.encode(PlayerDisconnect(self.player.id))
        self._broadcast_message(disconnect)

    def _broadcast_message(self, message) -> None:
        print(f"Broadcasting message {message}")
        for c in self.factory.clients:
            if c != self:
                c.transport.write(message)
