from enum import Enum
from typing import Any, Callable
import json

from twisted.internet import protocol

from pudink.common.model import ConnectionError, PlayerUpdate
from pudink.common.translator import MessageTranslator


class ClientCallback(Enum):
    STARTED_CONNECTING = 0
    CONNECTION_FAILED = 1
    CONNECTION_SUCCESS = 2
    DATA_RECEIVED = 3

    def __str__(self):
        return self.name.lower().replace("_", " ")


class PudinkClient(protocol.Protocol):
    def __init__(self, registeredCallbacks) -> None:
        super().__init__()
        self.registered_callbacks = registeredCallbacks

    def connectionMade(self):
        self.factory.process_callback(ClientCallback.CONNECTION_SUCCESS, "Connected!")

    def dataReceived(self, data):
        message = MessageTranslator.decode(data)
        self.factory.process_callback(ClientCallback.DATA_RECEIVED, message)

    def connectionLost(self, reason):
        error = ConnectionError(reason.getErrorMessage())
        self.factory.process_callback(ClientCallback.CONNECTION_FAILED, error)

    def send_message(self, message: any) -> None:
        if type(message) != PlayerUpdate:
            print(f"Sending message: {message}")
        data = MessageTranslator.encode(message)
        self.transport.write(data)


class PudinkClientFactory(protocol.ClientFactory):
    protocol = PudinkClient

    def __init__(self, host: str = "localhost", port: int = 8000):
        self.client = None
        self.host = host
        self.port = port
        self.scene = None
        self.registeredCallbacks = {
            ClientCallback.STARTED_CONNECTING: {},
            ClientCallback.CONNECTION_FAILED: {},
            ClientCallback.CONNECTION_SUCCESS: {},
            ClientCallback.DATA_RECEIVED: {},
        }
        self.connecting = False
        self.connected = False

    def clientConnectionFailed(self, connector, reason):
        error = ConnectionError(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def clientConnectionLost(self, connector, reason):
        error = ConnectionError(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def startedConnecting(self, connector):
        self.process_callback(ClientCallback.STARTED_CONNECTING, "Connecting")

    def process_callback(self, event: ClientCallback, data: any) -> None:
        if event == ClientCallback.STARTED_CONNECTING:
            self.connecting = True
            self.connected = False
        elif event == ClientCallback.CONNECTION_SUCCESS:
            self.connecting = False
            self.connected = True
        elif event == ClientCallback.CONNECTION_FAILED:
            self.connecting = False
            self.connected = False
        if self.scene in self.registeredCallbacks[event]:
            self.registeredCallbacks[event][self.scene](data)

    def registerCallback(
        self, event: ClientCallback, callback: Callable[[str], None], scene: str
    ):
        if event in self.registeredCallbacks:
            self.registeredCallbacks[event][scene] = callback
        else:
            self.registeredCallbacks[event] = {scene: callback}

    def buildProtocol(self, addr):
        print(f"Building protocol for {addr}")
        client = PudinkClient(self.registeredCallbacks)
        client.factory = self
        if self.client is not None:
            raise ConnectionError("Client already built")
        self.client = client
        return client

    def connect(self, host: str, port: int):
        from twisted.internet import reactor

        if not self.connecting and not self.connected:
            reactor.connectTCP(host, port, self)

    def set_scene(self, scene):
        self.scene = scene
