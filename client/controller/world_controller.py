from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from client.controller.base_controller import BaseController
from client.frontend.scene_manager import SceneManager
from client.game.world_state import WorldState

if TYPE_CHECKING:
    from client.game.client_factory import PudinkClientFactory

from client.game.client import ClientCallback
from common.model import ChatMessage, Player, PlayerDisconnect, PlayerUpdate


class WorldController(BaseController):
    """
    Controller class for managing the game world.

    This class handles player joining, leaving, and updating, as well as sending and receiving chat messages.

    Attributes:
        on_player_join_callback (Optional[Callable[[Player], None]]): Callback function called when a player joins.
        on_player_leave_callback (Optional[Callable[[PlayerDisconnect], None]]): Callback function called when a player leaves.
        on_player_update_callback (Optional[Callable[[PlayerUpdate], None]]): Callback function called when a player updates.
        on_chat_message_callback (Optional[Callable[[ChatMessage], None]]): Callback function called when a chat message is received.
    """

    on_player_join_callback: Callable[[Player], None] | None = None
    on_player_leave_callback: Callable[[PlayerDisconnect], None] | None = None
    on_player_update_callback: Callable[[PlayerUpdate], None] | None = None
    on_chat_message_callback: Callable[[ChatMessage], None] | None = None

    def __init__(
        self,
        factory: PudinkClientFactory,
        scene_manager: SceneManager,
        world_state: WorldState,
    ) -> None:
        """
        Initialize the WorldController.

        Args:
            factory (PudinkClientFactory): The client factory.
            scene_manager (SceneManager): The scene manager.
            world_state (WorldState): The world state.
        """
        super().__init__(factory, scene_manager, "world")
        self.world_state = world_state
        self.register_callback(
            ClientCallback.DATA_RECEIVED, self._on_update, self.scene
        )
        self.register_callback(
            ClientCallback.CONNECTION_FAILED, self._on_disconnect, self.scene
        )

        self.on_player_join_callback = None
        self.on_player_update_callback = None
        self.on_player_leave_callback = None
        self.on_chat_message_callback = None

    def move_player(self, new_x: int, new_y: int) -> None:
        """
        Move the current player to the specified coordinates.

        Args:
            new_x (int): The new x-coordinate.
            new_y (int): The new y-coordinate.
        """
        player = self.get_current_player()
        if player is None:
            print("No player found when trying to move")
            return
        update = PlayerUpdate(player.id, new_x, new_y)
        self._on_player_update(update)
        self.send_message(update)

    def send_chat_message(self, message: str) -> None:
        """
        Send a chat message from the current player.

        Args:
            message (str): The chat message.
        """
        player = self.get_current_player()
        if player is None:
            print("No player found when trying to send chat message")
            return
        chat_message = ChatMessage(player.id, message)
        self.send_message(chat_message)

    def _on_update(self, message: Any) -> None:
        """
        Handle incoming data received from the server.

        Args:
            message (Any): The received message.
        """
        if isinstance(message, PlayerDisconnect):
            self._on_player_leave(message)
        elif isinstance(message, Player):
            self._on_player_join(message)
        elif isinstance(message, PlayerUpdate):
            self._on_player_update(message)
        elif isinstance(message, ChatMessage):
            self._on_chat_message(message)
        else:
            print(f"Received unexpected message: {message}")

    def get_current_player(self) -> Player | None:
        """
        Get the current player.

        Returns:
            Optional[Player]: The current player, or None if no player is found.
        """
        return self.world_state.get_current_player()

    def get_player(self, player_id: str) -> Player | None:
        """
        Get a player by their ID.

        Args:
            player_id (str): The ID of the player.

        Returns:
            Optional[Player]: The player with the specified ID, or None if no player is found.
        """
        return self.world_state.get_player(player_id)

    def get_players(self) -> dict[str, Player]:
        """
        Get all players in the world.

        Returns:
            dict[str, Player]: A dictionary of players, where the keys are player IDs and the values are Player objects.
        """
        return self.world_state.get_players()

    def _on_player_join(self, new_player: Player) -> None:
        """
        Handle a player joining the world. Update the world state and call the player join callback.

        Args:
            new_player (Player): The new player.
        """
        self.world_state.add_player(new_player)
        if self.on_player_join_callback:
            self.on_player_join_callback(new_player)

    def _on_player_leave(self, disconnected_player: PlayerDisconnect) -> None:
        """
        Handle a player leaving the world. Update the world state and call the player leave callback.

        Args:
            disconnected_player (PlayerDisconnect): The disconnected player.
        """
        self.world_state.remove_player(disconnected_player)
        if self.on_player_leave_callback:
            self.on_player_leave_callback(disconnected_player)

    def _on_player_update(self, update: PlayerUpdate) -> None:
        """
        Handle a player update by updating the world state.
        If any callback is registered, call it with the update.

        Args:
            update (PlayerUpdate): The player update.
        """
        self.world_state.update_player(update)
        if self.on_player_update_callback:
            self.on_player_update_callback(update)

    def _on_chat_message(self, message: ChatMessage) -> None:
        """
        Handle a chat message by calling the chat message callback.

        Args:
            message (ChatMessage): The chat message.
        """
        if self.on_chat_message_callback:
            self.on_chat_message_callback(message)

    def _on_disconnect(self, data) -> None:
        """
        Handle a disconnection from the server.
        Switches to the menu screen.

        Args:
            data: The disconnection data.
        """
        print(f"Disconnected from server with message: {data}")
        self.switch_screen("menu")
