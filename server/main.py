from fastapi import FastAPI
from anime.api import AnimeAPI
from os import environ
from anime.cache import Cache
from anime.config import get_mal_client_id

app = FastAPI()
client_id = get_mal_client_id()
cache = Cache()
api = AnimeAPI(client_id,cache) 

@app.get('/')
def root():
    return {"status": "ok"}

@app.get("/anime/search")
def anime_search(q: str):
    return api.search_anime(q)

@app.get("/anime/{anime_id}")
def anime_get(anime_id: int):
    return api.get_anime(anime_id)
