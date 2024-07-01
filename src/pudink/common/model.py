from dataclasses import dataclass, field


# Sent from server to client when an error occurs
@dataclass
class ConnectionFailure:
    message: str


# Sent from client to server during login
@dataclass
class Credentials:
    name: str
    password: str


# Describes the character's appearance
@dataclass
class Character:
    head_type: int = field(metadata={"range": (1, 5)})
    body_type: int = field(metadata={"range": (1, 5)})

    def __post_init__(self):
        if not (self.head_type in range(1, 6)):
            raise ValueError(
                f"head_type must be between 1 and 5. Given: {self.head_type}"
            )
        if not (self.body_type in range(1, 6)):
            raise ValueError(
                f"body_type must be between 1 and 5. Given: {self.body_type}"
            )


# Sent from client to server during account creation
@dataclass
class NewAccount:
    name: str
    password: str
    character: Character


# Used for initializing player data on origin client
@dataclass
class PlayerInitialization:
    id: int
    character: Character


# Used for informing other players that a player has disconnected
@dataclass
class PlayerDisconnect:
    id: int


# Used for initializing player data on other clients
@dataclass
class Player:
    id: int
    character: Character
    x: int
    y: int


# Used for sending player data to other clients
@dataclass
class PlayerUpdate:
    id: int
    x: int
    y: int


# Sent from server to client during login
@dataclass
class PlayerSnapshot:
    current_player_id: int
    players: list[Player]


# Sent from client to server when a chat message is sent
@dataclass
class ChatMessage:
    player_id: int
    message: str
