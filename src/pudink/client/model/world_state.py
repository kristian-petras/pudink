from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from pudink.common.model import Player, PlayerDisconnect, PlayerSnapshot, PlayerUpdate


@dataclass
class WorldState:
    current_player_id: str = None
    players: Dict[str, Player] = field(default_factory=dict)

    def add_player(self, player: Player) -> None:
        """Adds a player to the game."""
        self.players[player.id] = player

    def remove_player(self, disconnect: PlayerDisconnect) -> None:
        """Removes a player from the game."""
        if disconnect.id not in self.players:
            raise ValueError(f"Player ID '{disconnect.id}' does not exist.")
        self.players.pop(disconnect.id)

    def update_player(self, update: PlayerUpdate) -> None:
        """Updates the location of a player."""
        if update.id not in self.players:
            raise ValueError(f"Player ID '{update.id}' does not exist.")
        self.players[update.id].x = update.x
        self.players[update.id].y = update.y

    def get_player(self, player_id: str) -> Player:
        """Gets the location of a specific player."""
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        return self.players[player_id]

    def get_all_players(self) -> Dict[str, Player]:
        """Returns all players and their locations."""
        return self.players

    def get_current_player(self) -> Optional[Player]:
        """Returns the current player."""
        if self.current_player_id is None:
            return None
        return self.players[self.current_player_id]

    def initialize_world(self, snapshot: PlayerSnapshot):
        """Initializes the game world with a snapshot."""
        for player in snapshot.players.values():
            self.players[player.id] = player
        self.current_player_id = snapshot.current_player_id
