from pudink.client.game import PudinkGame
from pudink.client.protocol.client_factory import PudinkClientFactory
from pyglet.window import Window


def main():
    game = PudinkGame(window=Window(600, 900, "Pudink"), factory=PudinkClientFactory())
    game.run()
    print("Game finished")


if __name__ == "__main__":
    main()
