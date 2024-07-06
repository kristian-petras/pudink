from typing import Dict, Optional

from pyglet.window import Window

from pudink.client.renderer.base_renderer import BaseRenderer


class SceneManager:
    """
    A class that manages scenes in a game or application.

    Attributes:
        window (Window): The main window of the application.
        scenes (Dict[str, BaseRenderer]): A dictionary that maps scene names to scene renderers.
        current_scene (Optional[BaseRenderer]): The currently active scene.

    Methods:
        __init__(self, window): Initializes the SceneManager with the main window.
        register_scene(self, name, scene): Registers a scene with the given name and scene renderer.
        switch_to_scene(self, name): Switches to the scene with the given name.
        on_draw(self): Renders the current scene.
        on_key_press(self, symbol, modifiers): Handles key press events for the current scene.
    """

    window: Window
    scenes: Dict[str, BaseRenderer]
    current_scene: Optional[BaseRenderer]

    def __init__(self, window) -> None:
        self.window = window
        self.scenes = {}
        self.current_scene = None

    def register_scene(self, name: str, scene: BaseRenderer) -> None:
        """
        Registers a scene with the given name and scene renderer.

        Args:
            name (str): The name of the scene.
            scene (BaseRenderer): The renderer for the scene.
        """
        self.scenes[name] = scene

    def switch_to_scene(self, name: str) -> None:
        """
        Switches to the scene with the given name.

        Args:
            name (str): The name of the scene to switch to.
        """
        if name in self.scenes:
            old_scene = self.current_scene
            if old_scene is not None:
                old_scene.before_scene_switch()
            self.current_scene = self.scenes[name]
            self.current_scene.after_scene_switch()
            print(f"Switched to screen '{name}'")

    def on_draw(self) -> None:
        """
        Renders the current scene.
        """
        if self.current_scene:
            self.current_scene.on_draw()

    def on_key_press(self, symbol, modifiers) -> None:
        """
        Handles key press events for the current scene.

        Args:
            symbol: The key symbol of the pressed key.
            modifiers: The modifiers (e.g., shift, alt) pressed along with the key.
        """
        if self.current_scene:
            self.current_scene.on_key_press(symbol, modifiers)
