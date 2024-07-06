import pyglet
from pyglet.graphics import Group
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout

from pudink.client.frontend.password_document import PasswordDocument


class PasswordTextEntry(pyglet.gui.TextEntry):
    """
    A custom text entry widget for entering passwords.

    Args:
        text (str): The initial text of the text entry.
        x (int): The x-coordinate of the text entry.
        y (int): The y-coordinate of the text entry.
        width (int): The width of the text entry.
        color (tuple, optional): The background color of the text entry. Defaults to (255, 255, 255, 255).
        text_color (tuple, optional): The text color of the text entry. Defaults to (0, 0, 0, 255).
        caret_color (tuple, optional): The caret color of the text entry. Defaults to (0, 0, 0, 255).
        batch (pyglet.graphics.Batch, optional): The batch to which the text entry belongs. Defaults to None.
        group (pyglet.graphics.Group, optional): The group to which the text entry belongs. Defaults to None.
    """

    def __init__(
        self,
        text,
        x,
        y,
        width,
        color=(255, 255, 255, 255),
        text_color=(0, 0, 0, 255),
        caret_color=(0, 0, 0, 255),
        batch=None,
        group=None,
    ):
        super().__init__(
            text, x, y, width, color, text_color, caret_color, batch, group
        )
        fg_group = Group(order=1, parent=group)

        self._doc = PasswordDocument(text)
        self._doc.set_style(0, len(self._doc.text), dict(color=text_color))
        font = self._doc.get_font()
        height = font.ascent - font.descent
        self._layout = IncrementalTextLayout(
            self._doc, width, height, multiline=False, batch=batch, group=fg_group
        )
        self._layout.x = x
        self._layout.y = y

        self._caret = Caret(self._layout, color=caret_color)

    def get_password(self) -> str:
        """
        Get the entered password.

        Returns:
            str: The entered password.
        """
        return self._doc._text
