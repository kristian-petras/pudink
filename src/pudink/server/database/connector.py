import os
import sqlite3
from typing import Optional, List

from pudink.common.model import Character, PlayerInitialization


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
        self, username: str, password: str, character_id: int
    ) -> Optional[PlayerInitialization]:
        pass

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional[PlayerInitialization]:
        query = "SELECT id, character_id FROM players WHERE username=? AND password=?"
        params = (username, password)
        self._cursor.execute(query, params)

        if row := self._cursor.fetchone():
            return PlayerInitialization(row[0], self._get_character_by_id(row[1]))

        return None

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
