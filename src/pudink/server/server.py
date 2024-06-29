import signal, os

from twisted.internet import reactor

from pudink.server.protocol.server import PudinkServer
from pudink.server.database.connector import GameDatabase

from twisted.internet.error import ReactorNotRunning
from sqlite3 import ProgrammingError


class PudinkServerRunner:
    def __init__(self, factory: PudinkServer, db_location: str, port: int = 8000):
        self._factory = factory
        self._db = GameDatabase(db_location)
        self._port = port

    def run(self):
        reactor.listenTCP(self._port, self._factory)
        signal.signal(signal.SIGINT, self._sigint_handler)
        print(f"Server started, listening on port {self._port}")
        reactor.run()

    def _sigint_handler(self, *args, **kwargs):
        print("SIGINT detected, shutting down.")
        try:
            reactor.stop()
            self._db.close_connection()
        except ReactorNotRunning:
            print("Reactor already closed.")
        except ProgrammingError:
            print("Database already closed.")
