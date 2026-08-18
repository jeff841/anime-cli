from fastapi import FastAPI, HTTPException
from .cache import Cache
from .mal import MALAPI

app = FastAPI(title="anime-cli API")

cache = Cache()
api = MALAPI(cache)


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
