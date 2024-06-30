from typing import Optional
from pyglet.resource import image
from pyglet.image import Texture


class AssetManager:
    def __init__(self) -> None:
        self._head_mapping = {
            1: image("simple_head.png"),
            2: image("monkey_head.png"),
            3: image("cow_head.png"),
            4: image("scary_head.png"),
            5: image("minecraft_head.png"),
        }
        self._body_mapping = {
            1: image("human_body.png"),
            2: image("monkey_body.png"),
            3: image("woman_body.png"),
            4: image("long_body.png"),
            5: image("minecraft_body.png"),
        }

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
