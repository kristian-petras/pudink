import pyglet

window = pyglet.window.Window(540, 500, caption="Widget Example")

pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1.0)


class Screen:
    def __init__(self, window: pyglet.window.Window) -> None:
        self.window = window
        self.batch = pyglet.graphics.Batch()

    def draw(self) -> None:
        self.window.clear()
        self.batch.draw()

    def add_element(self, element) -> None:
        element.batch = self.batch


class GameManager:
    def __init__(self, screen: Screen) -> None:
        self.screen = screen

    def on_draw(self) -> None:
        self.screen.on_draw()

    def switch_screen(self, screen: Screen) -> None:
        self.screen = screen

    def on_key_press(self, symbol, modifiers) -> None:
        self.screen.on_key_press(symbol, modifiers)


class LoginScreen:
    def __init__(self, window) -> None:
        self.screen = Screen(window)
        self.counter = 0
        self.counter_label = pyglet.text.Label(
            "Counter: 0",
            font_size=18,
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.screen.batch,
        )

    def on_draw(self) -> None:
        print("Drawing login screen")
        self.screen.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == pyglet.window.key.SPACE:
            self.counter += 1
            self.counter_label.text = f"Counter: {self.counter}"


class GameScreen:
    def __init__(self, window) -> None:
        self.screen = Screen(window)

    def on_draw(self) -> None:
        print("Drawing game screen")
        self.screen.draw()

    def on_key_press(self, symbol, modifiers) -> None:
        pass


login_screen = LoginScreen(window)
game_screen = GameScreen(window)
game_manager = GameManager(login_screen)

circle1 = pyglet.shapes.Circle(
    100, 100, 50, color=(255, 0, 0), batch=login_screen.screen.batch
)
circle2 = pyglet.shapes.Circle(
    200, 100, 50, color=(0, 255, 0), batch=game_screen.screen.batch
)


@window.event
def on_draw():
    game_manager.on_draw()


@window.event
def on_key_press(symbol, modifiers):
    game_manager.on_key_press(symbol, modifiers)
    if symbol == pyglet.window.key.SPACE:
        if game_manager.screen == login_screen:
            print("Switching to game screen")
            game_manager.switch_screen(game_screen)
        else:
            print("Switching to login screen")
            game_manager.switch_screen(login_screen)


pyglet.app.run()
