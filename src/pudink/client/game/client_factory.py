from typing import Any, Callable, Optional

from twisted.internet import protocol
from twisted.internet.interfaces import IAddress

from pudink.client.game.client import ClientCallback, PudinkClient
from pudink.common.model import ConnectionFailure


class PudinkClientFactory(protocol.ClientFactory):
    """
    Factory class for creating PudinkClient instances and managing client connections.

    Attributes:
        protocol: The protocol class to be used for creating client instances.
        client: The current client instance.
        host: The host address to connect to.
        port: The port number to connect to.
        scene: The current scene.
        registeredCallbacks: A dictionary of registered callbacks for different events.
        connecting: A boolean indicating if the client is currently connecting.
        connected: A boolean indicating if the client is currently connected.

    Methods:
        __init__: Initializes the PudinkClientFactory instance.
        clientConnectionFailed: Callback method called when client connection fails.
        clientConnectionLost: Callback method called when client connection is lost.
        startedConnecting: Callback method called when client starts connecting.
        process_callback: Processes the registered callback for a specific event.
        register_callback: Registers a callback for a specific event and scene.
        buildProtocol: Builds the protocol for the client.
        connect: Connects the client to the specified host and port.
        set_scene: Sets the current scene for the client.
    """

    protocol: type[PudinkClient] = PudinkClient
    client: Optional[PudinkClient]
    host: str
    port: int
    scene: Optional[str]
    registeredCallbacks: dict[ClientCallback, dict[str, Callable[[Any], None]]]
    connecting: bool
    connected: bool

    def __init__(self, host: str = "localhost", port: int = 8000):
        """
        Initializes the PudinkClientFactory instance.

        Args:
            host: The host address to connect to. Defaults to "localhost".
            port: The port number to connect to. Defaults to 8000.
        """
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
        """
        Callback method called when client connection fails.

        Args:
            connector: The connector object.
            reason: The reason for the connection failure.
        """
        error = ConnectionFailure(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def clientConnectionLost(self, connector, reason):
        """
        Callback method called when client connection is lost.

        Args:
            connector: The connector object.
            reason: The reason for the connection loss.
        """
        error = ConnectionFailure(reason.getErrorMessage())
        self.process_callback(ClientCallback.CONNECTION_FAILED, error)
        self.client = None

    def startedConnecting(self, connector):
        """
        Callback method called when client starts connecting.

        Args:
            connector: The connector object.
        """
        self.process_callback(ClientCallback.STARTED_CONNECTING, "Connecting")

    def process_callback(self, event: ClientCallback, data: Any) -> None:
        """
        Processes the registered callback for a specific event.

        Args:
            event: The event for which the callback is registered.
            data: The data to be passed to the callback.
        """
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
        """
        Registers a callback for a specific event and scene.

        Args:
            event: The event for which the callback is registered.
            callback: The callback function to be registered.
            scene: The scene for which the callback is registered.
        """
        if event in self.registeredCallbacks:
            self.registeredCallbacks[event][scene] = callback
        else:
            self.registeredCallbacks[event] = {scene: callback}

    def buildProtocol(self, addr: IAddress) -> PudinkClient:
        """
        Builds the protocol for the client.

        Args:
            addr: The address of the client.

        Returns:
            The built PudinkClient protocol instance.
        """
        print(f"Building protocol for {addr}")
        client = PudinkClient(self.registeredCallbacks)
        client.factory = self
        if self.client is not None:
            raise ConnectionFailure("Client already built")
        self.client = client
        return client

    def connect(self, host: str, port: int):
        """
        Connects the client to the specified host and port.

        Args:
            host: The host address to connect to.
            port: The port number to connect to.
        """
        from twisted.internet import reactor

        if not self.connecting and not self.connected:
            reactor.connectTCP(host, port, self)  # type: ignore

    def set_scene(self, scene):
        """
        Sets the current scene for the client.

        Args:
            scene: The scene to be set.
        """
        self.scene = scene
