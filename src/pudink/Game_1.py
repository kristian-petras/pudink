from pudink.LoginScreen import LoginScreen


class Game:
    def __init__(self, window):
        self.window = window
        self.current_screen = LoginScreen(self)

    def _on_draw(self):
        self.window.clear()
        self.current_screen.on_draw()

    def _on_mouse_press(self, x, y, button, modifiers):
        self.current_screen.on_mouse_press(x, y, button, modifiers)

    def _on_mouse_release(self, x, y, button, modifiers):
        self.current_screen.on_mouse_release(x, y, button, modifiers)

    def _on_key_press(self, symbol, modifiers):
        self.current_screen.on_key_press(symbol, modifiers)

    def switch_to_screen(self, screen):
        self.current_screen = screen(self)
