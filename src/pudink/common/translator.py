import json
from pudink.common.model import (
    Character,
    Credentials,
    ConnectionError,
    NewAccount,
    Player,
    PlayerDisconnect,
    PlayerInitialization,
    PlayerSnapshot,
    PlayerUpdate,
)


class MessageTranslator:
    @staticmethod
    def decode(message: bytes) -> any:
        message = json.loads(message.decode("utf-8"))
        decode_map = {
            "error": MessageTranslator._decode_error,
            "credentials": MessageTranslator._decode_credentials,
            "new_account": MessageTranslator._decode_new_account,
            "player_initialization": MessageTranslator._decode_player_initialization,
            "player_disconnect": MessageTranslator._decode_player_disconnect,
            "player": MessageTranslator._decode_player,
            "player_update": MessageTranslator._decode_player_update,
            "player_snapshot": MessageTranslator._decode_player_snapshot,
        }
        return decode_map[message["type"]](message)

    @staticmethod
    def _decode_error(message: dict) -> ConnectionError:
        return ConnectionError(message["message"])

    @staticmethod
    def _decode_credentials(message: dict) -> Credentials:
        return Credentials(message["name"], message["password"])

    @staticmethod
    def _decode_new_account(message: dict) -> NewAccount:
        character = MessageTranslator._decode_character(message["character"])
        return NewAccount(
            message["name"],
            message["password"],
            character,
        )

    @staticmethod
    def _decode_player_initialization(message: dict) -> PlayerInitialization:
        character = MessageTranslator._decode_character(message["character"])
        return PlayerInitialization(
            message["id"],
            character,
        )

    @staticmethod
    def _decode_player_disconnect(message: dict) -> PlayerDisconnect:
        return PlayerDisconnect(message["id"])

    @staticmethod
    def _decode_player(message: dict) -> Player:
        character = MessageTranslator._decode_character(message["character"])
        return Player(
            message["id"],
            character,
            message["x"],
            message["y"],
        )

    @staticmethod
    def _decode_player_update(message: dict) -> PlayerUpdate:
        return PlayerUpdate(
            message["id"],
            message["x"],
            message["y"],
        )

    @staticmethod
    def _decode_player_snapshot(message: dict) -> PlayerSnapshot:
        players = []
        for player in message["players"]:
            players.append(MessageTranslator._decode_player(player))
        return PlayerSnapshot(message["current_player_id"], players)

    @staticmethod
    def _decode_character(message: dict) -> Character:
        return Character(
            message["head_type"],
            message["body_type"],
        )

    @staticmethod
    def _encode_character(message: Character) -> dict:
        return {
            "head_type": message.head_type,
            "body_type": message.body_type,
        }

    @staticmethod
    def _encode_error(message: ConnectionError) -> dict:
        return {"type": "error", "message": message.message}

    @staticmethod
    def _encode_credentials(message: Credentials) -> dict:
        return {
            "type": "credentials",
            "name": message.name,
            "password": message.password,
        }

    @staticmethod
    def _encode_new_account(message: NewAccount) -> dict:
        character = MessageTranslator._encode_character(message.character)
        return {
            "type": "new_account",
            "name": message.name,
            "password": message.password,
            "character": character,
        }

    @staticmethod
    def _encode_player_initialization(message: PlayerInitialization) -> dict:
        character = MessageTranslator._encode_character(message.character)
        return {
            "type": "player_initialization",
            "id": message.id,
            "character": character,
        }

    @staticmethod
    def _encode_player_disconnect(message: PlayerDisconnect) -> dict:
        return {"type": "player_disconnect", "id": message.id}

    @staticmethod
    def _encode_player(message: Player) -> dict:
        character = MessageTranslator._encode_character(message.character)
        return {
            "type": "player",
            "id": message.id,
            "character": character,
            "x": message.x,
            "y": message.y,
        }

    @staticmethod
    def _encode_player_update(message: PlayerUpdate) -> dict:
        return {
            "type": "player_update",
            "id": message.id,
            "x": message.x,
            "y": message.y,
        }

    @staticmethod
    def _encode_player_snapshot(message: PlayerSnapshot) -> dict:
        players = []
        for player in message.players:
            players.append(MessageTranslator._encode_player(player))
        return {
            "type": "player_snapshot",
            "current_player_id": message.current_player_id,
            "players": players,
        }

    @staticmethod
    def encode(message: any) -> bytes:
        encode_map = {
            ConnectionError: MessageTranslator._encode_error,
            Credentials: MessageTranslator._encode_credentials,
            NewAccount: MessageTranslator._encode_new_account,
            Player: MessageTranslator._encode_player,
            PlayerInitialization: MessageTranslator._encode_player_initialization,
            PlayerDisconnect: MessageTranslator._encode_player_disconnect,
            PlayerUpdate: MessageTranslator._encode_player_update,
            PlayerSnapshot: MessageTranslator._encode_player_snapshot,
        }
        return json.dumps(encode_map[type(message)](message)).encode("utf-8")
