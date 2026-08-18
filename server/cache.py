from json import dumps, loads
from pathlib import Path
from sqlite3 import connect
from threading import RLock
from time import time


class Cache:
    """SQLite cache used by the hosted API.

    The cache lives in /tmp inside the Render container by default. It is
    intentionally ephemeral: losing it on a restart only causes the server
    to fetch the data from MAL again.
    """

    def __init__(self, path="/tmp/anime/cache.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = connect(self.path, check_same_thread=False)
        self.lock = RLock()
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                expires_at REAL NOT NULL
            )
            """
        )
        self.connection.commit()

    def get(self, key):
        with self.lock:
            row = self.connection.execute(
                "SELECT data, expires_at FROM cache WHERE key = ?",
                (key,),
            ).fetchone()
            if row is None:
                return None

            data, expires_at = row
            if time() >= expires_at:
                self.delete(key)
                return None

            return loads(data)

    def set(self, key, data, ttl):
        with self.lock:
            expires_at = time() + ttl
            self.connection.execute(
                """
                INSERT OR REPLACE INTO cache
                (key, data, expires_at)
                VALUES (?, ?, ?)
                """,
                (key, dumps(data), expires_at),
            )
            self.connection.commit()

    def delete(self, key):
        with self.lock:
            self.connection.execute(
                "DELETE FROM cache WHERE key = ?",
                (key,),
            )
            self.connection.commit()
