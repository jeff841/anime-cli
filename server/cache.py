from json import dumps, loads
from os import environ
from pathlib import Path
from sqlite3 import connect
from time import time


class Cache:
    """SQLite cache used by the hosted API.

    The database path can be configured with CACHE_DB_PATH. Render's
    filesystem is ephemeral unless a persistent disk is attached, so the
    default location is /tmp/anime/cache.db.
    """

    def __init__(self, path=None):
        path = path or environ.get("CACHE_DB_PATH", "/tmp/anime/cache.db")
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = connect(self.path, timeout=30.0)
        self.connection.execute("PRAGMA busy_timeout = 30000")
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
        self.connection.execute(
            "DELETE FROM cache WHERE key = ?",
            (key,),
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
