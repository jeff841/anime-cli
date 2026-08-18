from json import dumps, loads
from os import environ
from pathlib import Path
from sqlite3 import connect
from time import perf_counter, time


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
        started = perf_counter()

        with self._connect() as connection:
            row = connection.execute(
                "SELECT data, expires_at FROM cache WHERE key = ?",
                (key,),
            ).fetchone()

            if row is None:
                print(
                    f"CACHE MISS: {key} "
                    f"({(perf_counter() - started) * 1000:.1f}ms)",
                    flush=True,
                )
                return None

            data, expires_at = row

            if time() >= expires_at:
                connection.execute(
                    "DELETE FROM cache WHERE key = ?",
                    (key,),
                )
                print(
                    f"CACHE MISS (EXPIRED): {key} "
                    f"({(perf_counter() - started) * 1000:.1f}ms)",
                    flush=True,
                )
                return None

            result = loads(data)

        print(
            f"CACHE HIT: {key} "
            f"({(perf_counter() - started) * 1000:.1f}ms)",
            flush=True,
        )

        return result

    def set(self, key, data, ttl):
        started = perf_counter()
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

        print(
            f"CACHE SET: {key} "
            f"(TTL={ttl}s, {(perf_counter() - started) * 1000:.1f}ms)",
            flush=True,
        )

    def delete(self, key):
        started = perf_counter()

        with self._connect() as connection:
            connection.execute(
                "DELETE FROM cache WHERE key = ?",
                (key,),
            )

        print(
            f"CACHE DELETE: {key} "
            f"({(perf_counter() - started) * 1000:.1f}ms)",
            flush=True,
        )
