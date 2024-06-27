class SceneManager:
    def __init__(self, window):
        self.window = window
        self.scenes = {}
        self.current_scene = None

    def register_scene(self, name, scene):
        self.scenes[name] = scene

    def switch_to_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def on_draw(self):
        if self.current_scene:
            self.current_scene.on_draw()

    def on_key_press(self, symbol, modifiers):
        if self.current_scene:
            self.current_scene.on_key_press(symbol, modifiers)
