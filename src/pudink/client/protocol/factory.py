from enum import Enum
from typing import Any, Callable
import json

from twisted.internet import protocol


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
        self.factory._process_callback(ClientCallback.CONNECTION_SUCCESS, "Connected")

    def dataReceived(self, data):
        self.factory._process_callback(ClientCallback.DATA_RECEIVED, data.decode())

    def connectionLost(self, reason):
        self.factory._process_callback(
            ClientCallback.CONNECTION_FAILED, reason.getErrorMessage()
        )

    def send_message(self, msg):
        print(f"Sending message: {msg}")
        data = json.dumps(msg)
        self.transport.write(data.encode())


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
        self._process_callback(
            ClientCallback.CONNECTION_FAILED, reason.getErrorMessage()
        )

    def clientConnectionLost(self, connector, reason):
        self._process_callback(
            ClientCallback.CONNECTION_FAILED, reason.getErrorMessage()
        )

    def startedConnecting(self, connector):
        self._process_callback(ClientCallback.STARTED_CONNECTING, "Connecting")

    def _process_callback(self, event: ClientCallback, data: str):
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

    def registerCallback(self, event: ClientCallback, callback: Callable[[str], None]):
        self.registeredCallbacks[event] = {self.scene: callback}

    def buildProtocol(self, addr):
        client = PudinkClient(self.registeredCallbacks)
        client.factory = self
        if self.client is not None:
            raise ConnectionError("Client already built")
        self.client = client
        return client

    def connect(self):
        from twisted.internet import reactor

        if not self.connecting and not self.connected:
            reactor.connectTCP(self.host, self.port, self)

    def set_scene(self, scene):
        self.scene = scene
