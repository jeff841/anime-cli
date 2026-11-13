from time import perf_counter

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
    started = perf_counter()
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    result = api.search_anime(q)
    print(
        f"REQUEST /anime/search?q={q!r}: {(perf_counter() - started) * 1000:.1f}ms",
        flush=True,
    )
    return result


@app.get("/anime/{anime_id}")
def anime_get(anime_id: int):
    started = perf_counter()
    result = api.get_anime(anime_id)
    print(
        f"REQUEST /anime/{anime_id}: {(perf_counter() - started) * 1000:.1f}ms",
        flush=True,
    )
    return result
