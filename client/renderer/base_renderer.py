from typing import Callable, Optional

from pyglet.graphics import Batch, Group
from pyglet.gui import PushButton, TextEntry
from pyglet.image import Texture
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import Window

from client.frontend.asset_manager import AssetManager
from client.frontend.color_palette import ColorPalette
from client.frontend.password_text_entry import PasswordTextEntry


class BaseRenderer:
    """
    The base renderer class for rendering graphics and handling user input.

    Attributes:
        _handlers (list): A list of event handlers.

    Args:
        window (Window): The window object for rendering.
        asset_manager (AssetManager): The asset manager for accessing game assets.

    Methods:
        on_draw(): Clears the window and draws the batch.
        on_key_press(symbol, modifiers): Handles key press events.
        before_scene_switch(): Prepares for switching scenes by disabling event handlers.
        after_scene_switch(): Restores event handlers after switching scenes.
        create_entry(text, x, y, handler, width, password): Creates a text entry field.
        create_button(x, y, handler, pressed, depressed, hover): Creates a push button.
        create_label(x, y, text, width, multiline, anchor_x, anchor_y, align): Creates a label.
        create_sprite(texture, x, y): Creates a sprite.

    """

    _handlers: list

    def __init__(self, window: Window, asset_manager: AssetManager) -> None:
        self.window = window
        self.asset_manager = asset_manager
        self.batch = Batch()
        self.foreground_group = Group(1)
        self.background_group = Group(0)

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

    def after_scene_switch(self):
        for handler in self._handlers:
            handler.enabled = True
            self.window.push_handlers(handler)

    def create_entry(
        self,
        text: str,
        x: int,
        y: int,
        handler: Optional[Callable[[str], None]] = None,
        width: int = 200,
        password: bool = False,
    ) -> TextEntry:
        if password:
            entry = PasswordTextEntry(
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
        else:
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
        if handler is not None:
            entry.set_handler("on_commit", handler)
        self._handlers.append(entry)
        return entry

    def create_button(
        self,
        x: int,
        y: int,
        handler: Callable[[], None],
        pressed=None,
        depressed=None,
        hover=None,
    ) -> PushButton:
        button = PushButton(
            x,
            y,
            pressed=pressed or self.asset_manager.get_button_pressed(),
            depressed=depressed or self.asset_manager.get_button_depressed(),
            hover=hover or self.asset_manager.get_button_hover(),
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
        align="left",
    ) -> Label:
        return Label(
            text=text,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            width=width,
            multiline=multiline,
            batch=self.batch,
            align=align,
            color=ColorPalette.LIGHT.value,
            group=self.foreground_group,
        )

    def create_sprite(
        self,
        texture: Texture,
        x: int,
        y: int,
    ) -> Sprite:
        return Sprite(
            texture,
            x=x - texture.width // 2,
            y=y - texture.height // 2,
            batch=self.batch,
            group=self.foreground_group,
        )
