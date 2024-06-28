from pudink.client.model.player import Player


from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class WorldState:
    current_player_id: str
    players: Dict[str, Player] = field(default_factory=dict)

    def upsert_player(self, player: Player) -> None:
        """Adds a player to the game or updates an existing player."""
        self.players[player.id] = player

    def remove_player(self, player_id: str) -> None:
        """Removes a player from the game."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        del self.players[player_id]

    def get_player(self, player_id: str) -> Player:
        """Gets the location of a specific player."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        return self.players[player_id]

    def get_all_players(self) -> Dict[str, Player]:
        """Returns all players and their locations."""
        return self.players

    def get_current_player(self) -> Player:
        return self.players[self.current_player_id]

    def update(self, data) -> None:
        print(data)
