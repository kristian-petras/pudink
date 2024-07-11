from twisted.internet import protocol
from twisted.internet.interfaces import IAddress

from common.model import Player
from server.database.connector import GameDatabase
from server.protocol.pudink_connection import PudinkConnection


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
