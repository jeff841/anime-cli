from fastapi import FastAPI
from .mal import MyAnimeList
from os import environ
from .cache import Cache
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
cache = Cache()
mal = MyAnimeList(environ["MAL_CLIENT_ID"],cache)

@app.get('/')
def root():
    return {"status": "ok"}

@app.get("/anime/search")
async def anime_search(q: str):
    return await mal.search_anime(q)

@app.get("/anime/{anime_id}")
async def anime_get(anime_id: int):
    return await mal.get_anime(anime_id)
