import pyglet


class PasswordDocument(pyglet.text.document.UnformattedDocument):
    def __init__(self, text=""):
        super().__init__(text)

    @property
    def text(self):
        """Document text.

        For efficient incremental updates, use the :py:func:`~pyglet.text.document.AbstractDocument.insert_text` and
        :py:func:`~pyglet.text.document.AbstractDocument.delete_text` methods instead of replacing this property.

        :type: str
        """
        return "*" * len(self._text)
