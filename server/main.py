from fastapi import FastAPI, HTTPException
from anime.api import AnimeAPI
from anime.cache import Cache
from anime.config import get_mal_client_id

app = FastAPI(title="anime-cli API")

client_id = get_mal_client_id()
if not client_id:
    raise RuntimeError("MAL_CLIENT_ID is not configured on the server")

cache = Cache()
api = AnimeAPI(client_id, cache)


@app.get('/')
def root():
    return {"status": "ok"}


@app.get("/anime/search")
def anime_search(q: str):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    return api.search_anime(q)


@app.get("/anime/{anime_id}")
def anime_get(anime_id: int):
    return api.get_anime(anime_id)
