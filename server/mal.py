from httpx import Client

from .cache import Cache


class MALAPI:
    MAL_URL = "https://api.myanimelist.net/v2"

    def __init__(self, client_id: str, cache: Cache):
        self.headers = {"X-MAL-CLIENT-ID": client_id}
        self.cache = cache

    def search_anime(self, query: str):
        key = f"search:{query.strip().lower()}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        params = {"q": query, "limit": 10}
        with Client(timeout=15.0) as client:
            response = client.get(
                f"{self.MAL_URL}/anime",
                headers=self.headers,
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
            "fields": "title,main_picture,synopsis,num_episodes,mean,genres"
        }
        with Client(timeout=15.0) as client:
            response = client.get(
                f"{self.MAL_URL}/anime/{anime_id}",
                headers=self.headers,
                params=params,
            )
        response.raise_for_status()
        data = response.json()
        self.cache.set(key, data, ttl=60 * 60 * 24 * 7)
        return data
