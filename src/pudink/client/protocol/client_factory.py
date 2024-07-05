from typing import Any, Callable, Optional

from twisted.internet import protocol
from twisted.internet.interfaces import IAddress

from pudink.client.protocol.client import ClientCallback, PudinkClient
from pudink.common.model import ConnectionFailure


class PudinkClientFactory(protocol.ClientFactory):
    protocol: type[PudinkClient] = PudinkClient
    client: Optional[PudinkClient]
    host: str
    port: int
    scene: Optional[str]
    registeredCallbacks: dict[ClientCallback, dict[str, Callable[[Any], None]]]
    connecting: bool
    connected: bool

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
        error = ConnectionFailure(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def clientConnectionLost(self, connector, reason):
        error = ConnectionFailure(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def startedConnecting(self, connector):
        self.process_callback(ClientCallback.STARTED_CONNECTING, "Connecting")

    def process_callback(self, event: ClientCallback, data: Any) -> None:
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

    def register_callback(
        self, event: ClientCallback, callback: Callable[[Any], None], scene: str
    ):
        if event in self.registeredCallbacks:
            self.registeredCallbacks[event][scene] = callback
        else:
            self.registeredCallbacks[event] = {scene: callback}

    def buildProtocol(self, addr: IAddress) -> PudinkClient:
        print(f"Building protocol for {addr}")
        client = PudinkClient(self.registeredCallbacks)
        client.factory = self
        if self.client is not None:
            raise ConnectionFailure("Client already built")
        self.client = client
        return client

    def connect(self, host: str, port: int):
        from twisted.internet import reactor

        if not self.connecting and not self.connected:
            reactor.connectTCP(host, port, self)  # type: ignore

    def set_scene(self, scene):
        self.scene = scene
