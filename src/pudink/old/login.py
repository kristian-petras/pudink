import pyglet

from pudink.Game_1 import Game


def main():
    game = Game(pyglet.window.Window(800, 600, "Pudink"))

    @game.window.event
    def on_draw():
        game._on_draw()

    @game.window.event
    def on_key_press(symbol, modifiers):
        game._on_key_press(symbol, modifiers)

    @game.window.event
    def on_mouse_press(x, y, button, modifiers):
        game._on_mouse_press(x, y, button, modifiers)

    @game.window.event
    def on_mouse_release(x, y, button, modifiers):
        game._on_mouse_release(x, y, button, modifiers)

    pyglet.app.run()


main()
