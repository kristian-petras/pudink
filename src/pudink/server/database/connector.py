import os
import sqlite3
from typing import Optional, Union

from pudink.common.model import (
    Character,
    PlayerInitialization,
    ConnectionFailure,
    NewAccount,
    Credentials,
)


class GameDatabase:
    _instance = None

    def __new__(cls, db_file):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._db_file = db_file
            cls._instance._conn = None
            cls._instance._cursor = None
            cls._instance._initialize_database()
        return cls._instance

    def _initialize_database(self) -> None:
        self._conn = sqlite3.connect(self._db_file)
        self._cursor = self._conn.cursor()
        print(os.path.dirname(__file__))
        sql_file_location = os.path.join(
            os.path.dirname(__file__), "init_game_database.sql"
        )

        with open(sql_file_location) as sql_file:
            sql_script = sql_file.read()

        self._cursor.executescript(sql_script)
        self._conn.commit()
        print("Database initialized successfully")

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

            return PlayerInitialization(
                self._cursor.lastrowid,
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
            return PlayerInitialization(row[0], self._get_character_by_id(row[1]))

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
