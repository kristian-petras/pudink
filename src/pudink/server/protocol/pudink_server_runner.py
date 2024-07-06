import signal
from sqlite3 import ProgrammingError

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning

from pudink.server.database.connector import GameDatabase
from pudink.server.protocol.pudink_server import PudinkServer


class PudinkServerRunner:
    _db: GameDatabase
    _factory: PudinkServer
    _port: int

    def __init__(self, db_location: str, port: int = 8000) -> None:
        self._db = GameDatabase(db_location)
        self._factory = PudinkServer(self._db)
        self._port = port

    def run(self) -> None:
        reactor.listenTCP(self._port, self._factory)  # type: ignore
        signal.signal(signal.SIGINT, self._sigint_handler)
        print(f"Server started, listening on port {self._port}")
        reactor.run()  # type: ignore

    def _sigint_handler(self, *args, **kwargs) -> None:
        print("SIGINT detected, shutting down.")
        try:
            reactor.stop()  # type: ignore
            self._db.close_connection()
        except ReactorNotRunning:
            print("Reactor already closed.")
        except ProgrammingError:
            print("Database already closed.")
