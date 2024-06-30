from typing import Callable
from pyglet.graphics import Batch
from pyglet.graphics import Group
from pyglet.window import Window
from pyglet.sprite import Sprite
from pudink.client.asset_manager import AssetManager
from pudink.client.renderer.color_palette import ColorPalette
from pyglet.gui import TextEntry, PushButton
from pyglet.text import Label


class BaseRenderer:
    def __init__(self, window: Window, asset_manager: AssetManager) -> None:
        self.window = window
        self.asset_manager = asset_manager
        self.batch = Batch()
        self.foreground_group = Group()
        self.background_group = Group()

        self.background = asset_manager.get_background()
        self.background_sprite = Sprite(
            self.background,
            x=0,
            y=0,
            batch=self.batch,
            group=self.background_group,
        )
        self._handlers = []

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        pass

    def before_scene_switch(self):
        self.window.remove_handlers()
        for handler in self._handlers:
            handler.enabled = False

    def after_scene_switch(self, previous_scene):
        for handler in self._handlers:
            handler.enabled = True
            self.window.push_handlers(handler)

    def create_entry(self, text, x, y, handler: Callable[[str], None], width=150):
        entry = TextEntry(
            text=text,
            x=x,
            y=y,
            width=width,
            batch=self.batch,
            group=self.foreground_group,
            color=ColorPalette.LIGHT.value,
            text_color=ColorPalette.DARK.value,
            caret_color=ColorPalette.DARK.value,
        )
        entry.set_handler("on_commit", handler)
        self._handlers.append(entry)
        return entry

    def create_button(self, x: int, y: int, handler: Callable[[], None]):
        button = PushButton(
            x,
            y,
            pressed=self.asset_manager.get_button_pressed(),
            depressed=self.asset_manager.get_button_depressed(),
            hover=self.asset_manager.get_button_hover(),
            batch=self.batch,
            group=self.foreground_group,
        )
        button.set_handler("on_release", handler)
        self._handlers.append(button)
        return button

    def create_label(
        self,
        x,
        y,
        text,
        width=200,
        multiline=False,
        anchor_x="center",
        anchor_y="center",
    ):
        return Label(
            text=text,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            width=width,
            multiline=multiline,
            batch=self.batch,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )
