import os
from pudink.server.server import PudinkServer
from pudink.server.protocol.server import PudinkServer


def main():
    # TODO: config a nie v src =)
    db_location = os.path.join(os.path.dirname(__file__), "./database/game.db")

    server = PudinkServer(factory=PudinkServer(), db_location=db_location)
    server.run()


if __name__ == "__main__":
    main()
