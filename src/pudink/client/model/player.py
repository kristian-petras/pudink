from dataclasses import dataclass
from typing import Tuple


@dataclass
class Player:
    id: str
    username: str
    location: Tuple[float, float]
