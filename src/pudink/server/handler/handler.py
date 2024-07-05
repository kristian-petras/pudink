from __future__ import annotations
import json
from typing import Any, Callable
import typing
from pudink.common.model import (
    ConnectionFailure,
    NewAccount,
    Credentials,
    PlayerUpdate,
    PlayerSnapshot,
    ChatMessage,
    PlayerDisconnect,
)
from pudink.common.translator import MessageTranslator
from pudink.server.database.connector import GameDatabase

if typing.TYPE_CHECKING:
    from pudink.server.protocol.pudink_connection import PudinkConnection
    from pudink.server.protocol.pudink_server import PudinkServer


class BaseHandler:
    connection: PudinkConnection
    db: GameDatabase
    factory: PudinkServer
    message_handlers: dict[type, Callable[[Any], None]]

    def __init__(self, connection: PudinkConnection) -> None:
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

    def handle_message(self, message: Any) -> None:
        action = self.message_handlers[type(message)]
        if not action:
            raise NotImplemented(f"Unhandled message type: {type(message)}")

        action(message)

    def handle_new_account(self, message: NewAccount) -> None:
        raise NotImplemented()

    def handle_credentials(self, message: Credentials) -> None:
        raise NotImplemented()

    def handle_player_update(self, message: PlayerUpdate) -> None:
        raise NotImplemented()

    def handle_chat_message(self, message: ChatMessage) -> None:
        raise NotImplemented()

    def handle_player_disconnect(self, message: PlayerDisconnect) -> None:
        self.broadcast_message(message)

    def _send_error(self, error_message: ConnectionFailure) -> None:
        error = MessageTranslator.encode(error_message)
        self.connection.transport.write(error)

    def _send_player_snapshot(self) -> None:
        if not self.connection.player:
            self._send_error(ConnectionFailure("Player not initialized"))
            return

        players = list(self.factory.players.values())
        player_snapshot = PlayerSnapshot(self.connection.player.id, players)
        player_snapshot = MessageTranslator.encode(player_snapshot)

        self.connection.transport.write(player_snapshot)

    def broadcast_new_player(self) -> None:
        self.broadcast_message(self.connection.player)

    def broadcast_message(self, message: Any) -> None:
        if type(message) != bytes:
            message = MessageTranslator.encode(message)
        for c in self.factory.clients:
            if c != self.connection:
                c.transport.write(message)
