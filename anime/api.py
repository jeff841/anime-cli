from httpx import get

class AnimeAPI:
    def __init__(self,url):
        self.url = url

    def search_anime(self,query: str):
        response = get(
                f"{self.url}/anime/search",
                params={"q": query}
                )
        response.raise_for_status()
        return response.json()

    def get_anime(self,anime_id: int):
        response = get(
                f"{self.url}/anime/{anime_id}",
                )
        response.raise_for_status()
        return response.json()
