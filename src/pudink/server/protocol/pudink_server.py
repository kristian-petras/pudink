from pudink.common.model import Player
from pudink.server.database.connector import GameDatabase
from pudink.server.protocol.pudink_connection import PudinkConnection


from twisted.internet import protocol
from twisted.internet.interfaces import IAddress


class PudinkServer(protocol.ServerFactory):
    db: GameDatabase
    clients: list[PudinkConnection]
    players: dict[str, Player]

    def __init__(self, db: GameDatabase):
        self.db = db
        self.clients = []
        self.players = {}

    def buildProtocol(self, addr: IAddress):
        server_protocol = PudinkConnection(self.db, self)
        return server_protocol
