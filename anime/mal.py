from requests import get

class MyAnimeList:
    BASE_URL = "https://api.myanimelist.net/v2"

    def __init__(self,client_id):
        self.headers = {
                "X-MAL-CLIENT-ID": client_id
                }
    def search_anime(self,query,limit=10):
        response = get(
                f"{self.BASE_URL}/anime",
                headers=self.headers,
                params={
                    "q": query,
                    "limit": limit,
                    },
                )
        response.raise_for_status()
        return response.json()

    def get_anime(self,anime_id):
        response = get(
                f"{self.BASE_URL}/anime/{anime_id}",
                headers=self.headers,
                params={
                    "fields": "title,main_picture,synopsis,num_episodes,mean,genres"
                    },
                )
        response.raise_for_status()
        return response.json()
