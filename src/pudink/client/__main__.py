from pyglet.window import Window

from pudink.client.game.client_factory import PudinkClientFactory
from pudink.client.game.pudink_game import PudinkGame


def main():
    game = PudinkGame(window=Window(600, 900, "Pudink"), factory=PudinkClientFactory())
    game.run()
    print("Game finished")


if __name__ == "__main__":
    main()
