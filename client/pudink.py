from pyglet.window import Window

from client.game.client_factory import PudinkClientFactory
from client.game.pudink_game import PudinkGame


class Pudink:
    def run(self):
        game = PudinkGame(
            window=Window(600, 900, "Pudink"), factory=PudinkClientFactory()
        )
        game.run()
        print("Game finished")
