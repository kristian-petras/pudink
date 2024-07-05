from typing import Dict, Optional

from pyglet.window import Window

from pudink.client.renderer.base_renderer import BaseRenderer


class SceneManager:
    window: Window
    scenes: Dict[str, BaseRenderer]
    current_scene: Optional[BaseRenderer]

    def __init__(self, window) -> None:
        self.window = window
        self.scenes = {}
        self.current_scene = None

    def register_scene(self, name: str, scene: BaseRenderer) -> None:
        self.scenes[name] = scene

    def switch_to_scene(self, name: str) -> None:
        if name in self.scenes:
            old_scene = self.current_scene
            if old_scene is not None:
                old_scene.before_scene_switch()

            self.current_scene = self.scenes[name]
            self.current_scene.after_scene_switch()
            print(f"Switched to screen '{name}'")

    def on_draw(self) -> None:
        if self.current_scene:
            self.current_scene.on_draw()

    def on_key_press(self, symbol, modifiers) -> None:
        if self.current_scene:
            self.current_scene.on_key_press(symbol, modifiers)
