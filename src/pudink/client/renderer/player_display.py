from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, Group
from pyglet.image import Texture
from pyglet.shapes import Circle

from pudink.client.frontend.color_palette import ColorPalette


class PlayerDisplay:
    def __init__(
        self,
        x: int,
        y: int,
        head: Texture,
        body: Texture,
        batch: Batch,
        group: Group,
    ) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.group = group
        self.shadow = Circle(
            x=x + 48,
            y=y - 32,
            radius=32,
            color=ColorPalette.SHADOW.value,
            batch=batch,
            group=group,
        )
        self.body = Sprite(body, x=x, y=y - 32, batch=batch, group=group)
        self.head = Sprite(head, x=x, y=y + 63, batch=batch, group=group)
        self.chat_bubbles = []

    def create_chat_bubble(self, message: str) -> None:
        self.chat_bubbles.append(
            Label(
                message,
                x=self.x + 48,
                y=self.y + 160 + 32 * len(self.chat_bubbles),
                batch=self.batch,
                anchor_x="center",
                anchor_y="center",
                color=ColorPalette.LIGHT.value,
                group=self.group,
            )
        )

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.head.x = x
        self.head.y = y + 63
        self.body.x = x
        self.body.y = y - 32
        self.shadow.x = x + 48
        self.shadow.y = y - 32
        self._move_chat_bubbles(x, y)

    def pop_chat_bubble(self, _) -> None:
        self.chat_bubbles.pop(0).delete()
        self._move_chat_bubbles(self.x, self.y)

    def _move_chat_bubbles(self, x: int, y: int) -> None:
        for index, bubble in enumerate(self.chat_bubbles):
            bubble.x = x + 48
            bubble.y = y + 160 + 32 * index
