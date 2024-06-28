from pudink.client.model.player import Player


from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class WorldState:
    players: Dict[str, Player] = field(default_factory=dict)

    def add_player(self, player: Player) -> None:
        """Adds a new player to the game with their location."""
        if player.id in self.players:
            raise ValueError(f"Player ID '{player.id}' already exists.")
        self.players[player.id] = player

    def remove_player(self, player_id: str) -> None:
        """Removes a player from the game."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        del self.players[player_id]

    def update_location(
        self, player_id: str, new_location: Tuple[float, float]
    ) -> None:
        """Updates the location of an existing player."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        self.players[player_id].location = new_location

    def get_location(self, player_id: str) -> Tuple[float, float]:
        """Gets the location of a specific player."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        return self.players[player_id].location

    def get_all_players(self) -> Dict[str, Tuple[float, float]]:
        """Returns all players and their locations."""
        return self.players

    def update(self, data) -> None:
        print(data)
