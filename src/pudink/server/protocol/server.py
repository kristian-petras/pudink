from pudink.server.protocol.connection import PudinkConnection


from twisted.internet import protocol


class PudinkServer(protocol.ServerFactory):
    def __init__(self):
        self.clients = []
        self.players = []

    def buildProtocol(self, addr):
        server_protocol = PudinkConnection()
        server_protocol.factory = self

        return server_protocol
