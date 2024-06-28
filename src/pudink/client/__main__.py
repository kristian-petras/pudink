from pudink.client.game import PudinkGame
from pudink.client.protocol.factory import PudinkClientFactory
from pyglet.window import Window


def main():
    game = PudinkGame(window=Window(800, 600, "Pudink"), factory=PudinkClientFactory())
    game.run()
    print("Game finished")


if __name__ == "__main__":
    main()
