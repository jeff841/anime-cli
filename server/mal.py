from os import environ

from httpx import Client

from .cache import Cache


class MALAPI:
    MAL_URL = "https://api.myanimelist.net/v2"

    def __init__(self, cache: Cache):
        self.cache = cache
        self.client_id = environ["MAL_CLIENT_ID"].strip()
        if not self.client_id:
            raise RuntimeError("MAL_CLIENT_ID is not configured")

        self.client = Client(
            timeout=15.0,
            headers={
                "X-MAL-CLIENT-ID": self.client_id,
                "Accept": "application/json",
                "User-Agent": "anime-cli/0.1",
            },
        )

    def search_anime(self, query: str):
        key = f"search:{query.strip().lower()}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        params = {
            "q": query,
            "limit": 10,
        }
        response = self.client.get(
            f"{self.MAL_URL}/anime",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        results = [
            {
                "title": anime["node"]["title"],
                "id": anime["node"]["id"],
            }
            for anime in data["data"]
        ]
        self.cache.set(key, results, ttl=60 * 60 * 24)
        return results

    def get_anime(self, anime_id: int):
        key = f"anime:{anime_id}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        params = {
            "fields": "title,main_picture,synopsis,num_episodes,mean,genres",
        }
        response = self.client.get(
            f"{self.MAL_URL}/anime/{anime_id}",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        self.cache.set(key, data, ttl=60 * 60 * 24 * 7)
        return data

    def close(self):
        self.client.close()
