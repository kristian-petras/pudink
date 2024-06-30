from typing import Optional
from pyglet.resource import image
from pyglet.image import Texture
from pyglet.gl import glBindTexture, GL_TEXTURE_MAG_FILTER, GL_NEAREST, glTexParameteri


class AssetManager:
    def __init__(self) -> None:
        self._head_mapping = {
            1: self._init_image("simple_head.png"),
            2: self._init_image("monkey_head.png"),
            3: self._init_image("cow_head.png"),
            4: self._init_image("scary_head.png"),
            5: self._init_image("minecraft_head.png"),
        }
        self._body_mapping = {
            1: self._init_image("human_body.png"),
            2: self._init_image("monkey_body.png"),
            3: self._init_image("woman_body.png"),
            4: self._init_image("long_body.png"),
            5: self._init_image("minecraft_body.png"),
        }
        self._background = self._init_image("background.png")
        self._button_pressed = self._init_image("button_pressed.png")
        self._button_depressed = self._init_image("button_depressed.png")
        self._button_hover = self._init_image("button_hover.png")
        self._title = self._init_image("title.png")

        self._left = self._init_image("left.png")
        self._right = self._init_image("right.png")

    def get_head(self, head_id: int) -> Optional[Texture]:
        if head_id not in self._head_mapping:
            print(f"Head id {head_id} not found")
            return None
        return self._head_mapping[head_id]

    def get_body(self, body_id: int) -> Optional[Texture]:
        if body_id not in self._body_mapping:
            print(f"Body id {body_id} not found")
            return None
        return self._body_mapping[body_id]

    def _init_image(self, path: str) -> Texture:
        img = image(path)
        self._texture_set_mag_filter_nearest(img.get_texture())
        return img

    def _texture_set_mag_filter_nearest(self, texture):
        glBindTexture(texture.target, texture.id)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(texture.target, 0)

    def get_background(self) -> Texture:
        return self._background

    def get_button_pressed(self) -> Texture:
        return self._button_pressed

    def get_button_depressed(self) -> Texture:
        return self._button_depressed

    def get_button_hover(self) -> Texture:
        return self._button_hover

    def get_title(self) -> Texture:
        return self._title

    def get_heads(self):
        return self._head_mapping

    def get_bodies(self):
        return self._body_mapping

    def get_right(self) -> Texture:
        return self._right

    def get_left(self) -> Texture:
        return self._left
