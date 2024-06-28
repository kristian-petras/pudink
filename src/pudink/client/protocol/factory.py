from pudink.client.protocol.client import PudinkClient


from twisted.internet import protocol


class PudinkClientFactory(protocol.ClientFactory):
    protocol = PudinkClient

    def __init__(self):
        self.client = None

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")

    def buildProtocol(self, addr):
        p = PudinkClient()
        p.factory = self
        if self.client is not None:
            raise ConnectionError("Client already built")
        self.client = p
        return p
