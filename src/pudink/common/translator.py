import json
from pudink.common.model import (
    Credentials,
    Error,
    NewAccount,
    Player,
    PlayerDisconnect,
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
    def _decode_error(message: dict) -> Error:
        return Error(message["message"])

    @staticmethod
    def _decode_credentials(message: dict) -> Credentials:
        return Credentials(message["name"], message["password"])

    @staticmethod
    def _decode_new_account(message: dict) -> NewAccount:
        return NewAccount(
            message["name"],
            message["password"],
            message["head_type"],
            message["body_type"],
        )

    @staticmethod
    def _decode_player_initialization(message: dict) -> Player:
        return Player(
            message["id"],
            message["head_type"],
            message["body_type"],
        )

    @staticmethod
    def _decode_player_disconnect(message: dict) -> PlayerDisconnect:
        return PlayerDisconnect(message["id"])

    @staticmethod
    def _decode_player(message: dict) -> Player:
        return Player(
            message["id"],
            message["head_type"],
            message["body_type"],
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
    def _encode_error(message: Error) -> dict:
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
        return {
            "type": "new_account",
            "name": message.name,
            "password": message.password,
            "head_type": message.head_type,
            "body_type": message.body_type,
        }

    @staticmethod
    def _encode_player_initialization(message: Player) -> dict:
        return {
            "type": "player_initialization",
            "id": message.id,
            "head_type": message.head_type,
            "body_type": message.body_type,
        }

    @staticmethod
    def _encode_player_disconnect(message: PlayerDisconnect) -> dict:
        return {"type": "player_disconnect", "id": message.id}

    @staticmethod
    def _encode_player(message: Player) -> dict:
        return {
            "type": "player",
            "id": message.id,
            "head_type": message.head_type,
            "body_type": message.body_type,
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
            Error: MessageTranslator._encode_error,
            Credentials: MessageTranslator._encode_credentials,
            NewAccount: MessageTranslator._encode_new_account,
            Player: MessageTranslator._encode_player_initialization,
            PlayerDisconnect: MessageTranslator._encode_player_disconnect,
            PlayerUpdate: MessageTranslator._encode_player_update,
            PlayerSnapshot: MessageTranslator._encode_player_snapshot,
        }
        return json.dumps(encode_map[type(message)](message)).encode("utf-8")
