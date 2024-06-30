from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.image import Texture
from pyglet.clock import schedule_once


class PlayerDisplay:
    def __init__(
        self, x: int, y: int, head: Texture, body: Texture, batch: Batch
    ) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.head = Sprite(head, x=x, y=y + 32, batch=batch)
        self.body = Sprite(body, x=x, y=y, batch=batch)
        self.chat_bubbles = []

    def create_chat_bubble(self, message: str) -> None:
        self.chat_bubbles.append(
            Label(
                message,
                x=self.x,
                y=self.y + 32 + 20 * len(self.chat_bubbles),
                batch=self.batch,
                anchor_x="center",
                anchor_y="center",
                color=(0, 0, 0, 255),
            )
        )
        schedule_once(lambda _: self._pop_chat_bubble, 5)

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.head.x = x
        self.head.y = y + 32
        self.body.x = x
        self.body.y = y
        self._move_chat_bubbles(x, y)

    def _pop_chat_bubble(self) -> None:
        self.chat_bubbles.pop(0).delete()
        self._move_chat_bubbles(self.x, self.y)

    def _move_chat_bubbles(self, x: int, y: int) -> None:
        for index, bubble in enumerate(self.chat_bubbles):
            bubble.x = x
            bubble.y = y + 32 + 20 * index
