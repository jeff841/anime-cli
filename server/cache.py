from json import loads,dumps
from sqlite3 import connect
from time import time

class Cache:
    def __init__(self,path="cache.db"):
        self.connection = connect(path)
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
        """)
        self.connection.commit()

    def get(self,key):
        row = self.connection.execute(
                "SELECT data, expires_at FROM cache WHERE key = ?",
                (key,),
                ).fetchone()
        if row is None:
            return None
        data,expires_at = row
        if time() >= expires_at:
            self.delete(key)
            return None
        return loads(data)

    def set(self,key,data,ttl):
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

    def delete(self,key):
        self.connection.execute(
                "DELETE FROM cache WHERE key = ?",
                (key,),
                )
        self.connection.commit()
