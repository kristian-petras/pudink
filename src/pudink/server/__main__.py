import os

from pudink.server.protocol.pudink_server_runner import PudinkServerRunner


def main():
    # TODO: config file
    # TODO: logging support
    db_location = os.path.join(os.path.dirname(__file__), "./database/game.db")

    server = PudinkServerRunner(db_location=db_location)
    server.run()


if __name__ == "__main__":
    main()
