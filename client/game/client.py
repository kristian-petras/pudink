from __future__ import annotations

import typing
from enum import Enum
from typing import Any

from twisted.internet import protocol

if typing.TYPE_CHECKING:
    from pudink.client.game.client_factory import PudinkClientFactory

from pudink.common.model import ConnectionFailure, PlayerUpdate
from pudink.common.translator import MessageTranslator


class ClientCallback(Enum):
    STARTED_CONNECTING = 0
    CONNECTION_FAILED = 1
    CONNECTION_SUCCESS = 2
    DATA_RECEIVED = 3

    def __str__(self):
        return self.name.lower().replace("_", " ")


class PudinkClient(protocol.Protocol):
    """
    Represents a client for the Pudink protocol.

    This class handles the communication between the client and the server.
    """

    factory: PudinkClientFactory

    def __init__(self, registeredCallbacks) -> None:
        super().__init__()
        self.registered_callbacks = registeredCallbacks

    def connectionMade(self):
        self.factory.process_callback(ClientCallback.CONNECTION_SUCCESS, "Connected!")

    def dataReceived(self, data):
        message = MessageTranslator.decode(data)
        self.factory.process_callback(ClientCallback.DATA_RECEIVED, message)

    def connectionLost(self, reason):
        error = ConnectionFailure(reason.getErrorMessage())
        self.factory.process_callback(ClientCallback.CONNECTION_FAILED, error)

    def send_message(self, message: Any) -> None:
        if not isinstance(message, PlayerUpdate):
            print(f"Sending message: {message}")
        data = MessageTranslator.encode(message)
        self.transport.write(data)  # type: ignore
