from httpx import Client, HTTPStatusError, RequestError

from .constants import API_URL


class RemoteAnimeAPI:
    """Client for the hosted anime API.

    MAL authentication happens on the server. The CLI never receives or
    sends the MAL client ID.
    """

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, **params):
        try:
            with Client(timeout=15.0) as client:
                response = client.get(f"{self.base_url}{path}", params=params)
                response.raise_for_status()
                return response.json()
        except RequestError as exc:
            raise RuntimeError(
                f"Could not connect to the anime API at {self.base_url}"
            ) from exc
        except HTTPStatusError as exc:
            detail = exc.response.text.strip()
            raise RuntimeError(
                f"Anime API returned HTTP {exc.response.status_code}: {detail}"
            ) from exc

    def search_anime(self, query: str):
        return self._get("/anime/search", q=query.strip())

    def get_anime(self, anime_id: int):
        return self._get(f"/anime/{anime_id}")
