from dataclasses import dataclass


# Sent from server to client when an error occurs
@dataclass
class ConnectionError:
    message: str


# Sent from client to server during login
@dataclass
class Credentials:
    name: str
    password: str


# Describes the character's appearance
@dataclass
class Character:
    head_type: int
    body_type: int


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
