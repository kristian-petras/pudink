import os
import sqlite3
from typing import Optional, Union

from common.model import (
    Character,
    ConnectionFailure,
    Credentials,
    NewAccount,
    PlayerInitialization,
)


class GameDatabase:
    _instance = None
    _conn: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __new__(cls, db_file: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            conn, cursor = cls._instance._initialize_database(db_file)
            cls._instance._conn = conn
            cls._instance._cursor = cursor
        return cls._instance

    @staticmethod
    def _initialize_database(file: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        print(os.path.dirname(__file__))
        sql_file_location = os.path.join(
            os.path.dirname(__file__), "init_game_database.sql"
        )

        with open(sql_file_location) as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)
        conn.commit()
        print("Database initialized successfully")
        return conn, cursor

    def register_user(
        self, account_request: NewAccount
    ) -> Union[PlayerInitialization, ConnectionFailure]:
        try:
            self._conn.execute("BEGIN TRANSACTION")
            character_query = "INSERT INTO characters (head, body) VALUES (?, ?)"
            character_params = (
                account_request.character.head_type,
                account_request.character.body_type,
            )
            self._cursor.execute(character_query, character_params)
            character_id = self._cursor.lastrowid

            player_query = "INSERT INTO players (username, password, character_id) VALUES (?, ?, ?)"
            player_params = (
                account_request.name,
                account_request.password,
                character_id,
            )
            self._cursor.execute(player_query, player_params)
            self._conn.commit()

            print(
                f"User {account_request.name} registered successfully with character ID {character_id}"
            )

            id = self._cursor.lastrowid
            if id is None:
                raise sqlite3.IntegrityError(
                    "Failed to register user, could not get ID"
                )

            return PlayerInitialization(
                str(id),
                account_request.character,
            )
        except sqlite3.IntegrityError as e:
            self._conn.rollback()
            error = f"Failed to register user {account_request.name}: {e}"
            return ConnectionFailure(error)

    def authenticate_user(
        self, credentials: Credentials
    ) -> Union[PlayerInitialization, ConnectionFailure]:
        query = "SELECT id, character_id FROM players WHERE username=? AND password=?"
        params = (credentials.name, credentials.password)
        self._cursor.execute(query, params)

        if row := self._cursor.fetchone():
            character = self._get_character_by_id(row[1])
            if character is not None:
                return PlayerInitialization(row[0], character)

        return ConnectionFailure("Failed to authenticate user")

    def _get_character_by_id(self, character_id: int) -> Optional[Character]:
        query = "SELECT head, body FROM characters WHERE id=?"
        params = (character_id,)
        self._cursor.execute(query, params)

        if row := self._cursor.fetchone():
            return Character(row[0], row[1])

        return None

    def close_connection(self) -> None:
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
