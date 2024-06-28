import asyncio

from pudink.client.game import PudinkGame


def main():
    game = PudinkGame()
    game.run()
    print("Game finished")


if __name__ == "__main__":
    main()
