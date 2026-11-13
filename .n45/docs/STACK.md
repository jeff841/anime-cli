---
created_at: "2026-11-13 10:41:11"
layers:
    - items:
        architecture: 'Two parts: curses CLI client (anime/) and a small HTTP proxy server (server/) with SQLite cache'
        framework: FastAPI (metadata proxy server in server/)
        http_clients: httpx (sync in CLI, async in server), requests (cover image download)
      name: backend
      technology: Python 3.10+
    - items:
        migrations: none; CREATE TABLE IF NOT EXISTS at startup
        usage: server/cache.py key/value cache with TTL, file cache.db in the server working directory
      name: database
      technology: SQLite (stdlib sqlite3)
    - items:
        external_player: VLC executable found in PATH
        optional_terminal: kitty (kitten icat) for cover image display
        packaging: pyproject.toml, setuptools>=61, console script anime = anime.main:main
      name: infra
      technology: pip / setuptools
    - items:
        note: No test framework or test files exist in the repository
      name: tests
      technology: none configured
    - items:
        endpoints: GET /, GET /anime/search?q=, GET /anime/{anime_id}
        upstream: MyAnimeList API v2 using X-MAL-CLIENT-ID header
      name: api
      technology: REST (JSON)
n45_version: 1.1.0
updated_at: "2026-11-13 10:41:11"
---
