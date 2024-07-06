from dataclasses import dataclass, field
from typing import Dict, Optional

from pudink.common.model import Player, PlayerDisconnect, PlayerSnapshot, PlayerUpdate


@dataclass
class WorldState:
    """Represents the state of the game world."""

    current_player_id: Optional[str] = None
    players: Dict[str, Player] = field(default_factory=dict)

    def add_player(self, player: Player) -> None:
        """Adds a player to the game.

        Args:
            player (Player): The player to add.

        Returns:
            None
        """
        self.players[player.id] = player

    def remove_player(self, disconnect: PlayerDisconnect) -> None:
        """Removes a player from the game.

        Args:
            disconnect (PlayerDisconnect): The player to remove.

        Returns:
            None

        Raises:
            ValueError: If the player ID does not exist.
        """
        if disconnect.id not in self.players:
            raise ValueError(f"Player ID '{disconnect.id}' does not exist.")
        self.players.pop(disconnect.id)

    def update_player(self, update: PlayerUpdate) -> None:
        """Updates the location of a player.

        Args:
            update (PlayerUpdate): The updated player information.

        Returns:
            None

        Raises:
            ValueError: If the player ID does not exist.
        """
        if update.id not in self.players:
            raise ValueError(f"Player ID '{update.id}' does not exist.")
        self.players[update.id].x = update.x
        self.players[update.id].y = update.y

    def get_player(self, player_id: str) -> Player:
        """Gets the location of a specific player.

        Args:
            player_id (str): The ID of the player.

        Returns:
            Player: The player object.

        Raises:
            ValueError: If the player ID does not exist.
        """
        if player_id not in self.players:
            raise ValueError(f"Player ID '{player_id}' does not exist.")
        return self.players[player_id]

    def get_players(self) -> Dict[str, Player]:
        """Returns all players and their locations.

        Returns:
            Dict[str, Player]: A dictionary of player IDs and their corresponding player objects.
        """
        return self.players

    def get_current_player(self) -> Optional[Player]:
        """Returns the current player.

        Returns:
            Optional[Player]: The current player object, or None if there is no current player.
        """
        if self.current_player_id is None:
            return None
        return self.players[self.current_player_id]

    def initialize_world(self, snapshot: PlayerSnapshot):
        """Initializes the game world with a snapshot.

        Args:
            snapshot (PlayerSnapshot): The snapshot of the game world.

        Returns:
            None
        """
        for player in snapshot.players:
            self.players[player.id] = player
        self.current_player_id = snapshot.current_player_id
