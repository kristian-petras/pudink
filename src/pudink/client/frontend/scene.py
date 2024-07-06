from typing import Protocol


class Scene(Protocol):
    def on_draw(self): ...

    def on_key_press(self, symbol, modifiers): ...
