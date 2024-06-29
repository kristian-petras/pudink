from dataclasses import dataclass

from pudink.server.model.character import Character


@dataclass
class Player:
    id: int
    name: str
    character: Character
