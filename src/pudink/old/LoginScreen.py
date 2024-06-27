import pyglet
from pyglet.window import key

from pudink.HelloWorldScreen import HelloWorldScreen


class LoginScreen:
    def __init__(self, game):
        self.game = game
        self.batch = pyglet.graphics.Batch()
        width, height = self.game.window.get_size()

        self.username_label = pyglet.text.Label(
            "Username:",
            font_size=18,
            x=width // 2 - 100,
            y=height // 2 + 50,
            anchor_x="right",
            anchor_y="center",
            batch=self.batch,
        )

        frame = pyglet.gui.Frame(self.game.window)
        pressed = pyglet.image.load("assets/ui/blue_button05.png")
        pressed.anchor_x = pressed.width // 2
        pressed.anchor_y = pressed.height // 2
        depressed = pyglet.image.load("assets/ui/blue_button04.png")
        depressed.anchor_x = depressed.width // 2
        depressed.anchor_y = depressed.height // 2
        self.login_button = pyglet.gui.PushButton(
            x=width // 2,
            y=height // 2,
            pressed=pressed,
            depressed=depressed,
            batch=self.batch,
        )
        frame.add_widget(self.login_button)

        self.test = pyglet.text.Label(
            "Enter world",
            font_size=18,
            x=width // 2,
            y=height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        self.username_input = pyglet.text.Label(
            "",
            font_size=18,
            x=width // 2,
            y=height // 2 + 50,
            anchor_x="left",
            anchor_y="center",
            batch=self.batch,
        )

        self.password_label = pyglet.text.Label(
            "Password:",
            font_size=18,
            x=width // 2 - 100,
            y=height // 2,
            anchor_x="right",
            anchor_y="center",
            batch=self.batch,
        )

        self.password_input = pyglet.text.Label(
            "",
            font_size=18,
            x=width // 2,
            y=height // 2,
            anchor_x="left",
            anchor_y="center",
            batch=self.batch,
        )

        self.game.window.push_handlers(self.login_button)
        self.login_button.set_handler("on_press", self.my_on_press_handler)
        self.login_button.set_handler("on_release", self.my_on_release_handler)

    def my_on_press_handler(self):
        print("Button Pressed!")

    def my_on_release_handler(self):
        print("Button Released...")

    def on_login_button_click(self):
        print("Login button clicked!")

    def on_draw(self):
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.login_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.login_button.on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN:
            self.window.switch_to_screen(HelloWorldScreen)
        elif symbol == key.BACKSPACE:
            self.selected_input.text = self.username_input.text[:-1]
        else:
            self.selected_input.text += chr(symbol)
