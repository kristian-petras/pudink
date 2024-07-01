from pudink.server.database.connector import GameDatabase
from pudink.server.protocol.pudink_connection import PudinkConnection


from twisted.internet import protocol


class PudinkServer(protocol.ServerFactory):
    def __init__(self, db: GameDatabase):
        self.db = db
        self.clients = []
        self.players = {}

    def buildProtocol(self, addr):
        server_protocol = PudinkConnection(self.db, self)
        return server_protocol
