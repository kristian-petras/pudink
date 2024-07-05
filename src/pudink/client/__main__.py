from pyglet.window import Window

from pudink.client.game import PudinkGame
from pudink.client.protocol.client_factory import PudinkClientFactory


def main():
    game = PudinkGame(window=Window(600, 900, "Pudink"), factory=PudinkClientFactory())
    game.run()
    print("Game finished")


if __name__ == "__main__":
    main()
