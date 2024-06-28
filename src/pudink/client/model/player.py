from dataclasses import dataclass
from typing import Tuple


@dataclass
class Player:
    id: str
    location: Tuple[float, float]
