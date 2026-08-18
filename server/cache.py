from json import dumps, loads
from os import environ
from pathlib import Path
from sqlite3 import connect
from time import time


class Cache:
    """SQLite cache used by the hosted API.

    A connection is opened per operation so the cache is safe when FastAPI
    runs synchronous endpoints in different worker threads.
    """

    def __init__(self, path=None):
        path = path or environ.get("CACHE_DB_PATH", "/tmp/anime/cache.db")
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = connect(self.path, timeout=30.0)
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def _initialize(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    expires_at REAL NOT NULL
                )
                """
            )

    def get(self, key):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT data, expires_at FROM cache WHERE key = ?",
                (key,),
            ).fetchone()

            if row is None:
                return None

            data, expires_at = row
            if time() >= expires_at:
                connection.execute(
                    "DELETE FROM cache WHERE key = ?",
                    (key,),
                )
                return None

            return loads(data)

    def set(self, key, data, ttl):
        expires_at = time() + ttl
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO cache
                (key, data, expires_at)
                VALUES (?, ?, ?)
                """,
                (key, dumps(data), expires_at),
            )

    def delete(self, key):
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM cache WHERE key = ?",
                (key,),
            )
