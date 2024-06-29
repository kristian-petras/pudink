CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES characters(id)
);

CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    head INTEGER NOT NULL CHECK (head <= 5),
    body INTEGER NOT NULL CHECK (body <= 5),
    UNIQUE(head, body)
);

INSERT OR IGNORE INTO characters (head, body) VALUES (1, 1);
INSERT OR IGNORE INTO players (username, password, character_id) VALUES ('test', 'test', 1);
INSERT OR IGNORE INTO characters (head, body) VALUES (1, 2);
INSERT OR IGNORE INTO players (username, password, character_id) VALUES ('admin', 'admin', 2);