---
created_at: "2026-11-13 10:41:11"
n45_version: 1.1.0
patterns:
    - description: One small module per responsibility in the anime package; plain functions, one class per external client
      name: Layout
      scope: architecture
    - description: CLI calls the local FastAPI server (URL from ANIME_API_URL, config.json or default, resolved in anime/config.py) which proxies and caches MyAnimeList
      name: Client/server split
      scope: architecture
    - description: snake_case modules and functions, PascalCase classes, UPPER_SNAKE constants in constants.py
      name: Naming
      scope: code_conventions
    - description: Episodes are files named ep<N>-..., openings op<N>-, endings ed<N>-; suffix "watched" marks watched
      name: Episode files
      scope: code_conventions
    - description: Server URL resolved in anime/config.py - ANIME_API_URL env, then api_url in config.json, then http://127.0.0.1:8000; invalid values raise ConfigError (no fallback)
      name: Server URL resolution
      scope: architecture
    - description: Server cache keys search:<query> (TTL 1 day) and anime:<id> (TTL 7 days)
      name: Caching
      scope: architecture
updated_at: "2026-11-13 11:20:15"
---

## Architecture

**Responsibility of each part:**

- `anime/main.py`: argument parsing and the main loop; dispatches to other modules
- `anime/cli.py`: curses menu rendering; kitty image display
- `anime/show.py`, `play.py`, `extra.py`, `reset_watched.py`, `renamer.py`, `watch_input.py`: episode listing, playback, and file operations on the collection directory
- `anime/api.py`: HTTP client for the metadata server
- `anime/config.py`: resolves and validates the metadata server URL (env var, `config.json`, default)
- `server/`: FastAPI app (`main.py`), MyAnimeList client (`mal.py`), SQLite cache (`cache.py`)

**Folder structure:**

```
anime-cli/
├── anime/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api.py
│   ├── cli.py
│   ├── config.py
│   ├── constants.py
│   ├── episode.py
│   ├── extra.py
│   ├── kitty.py
│   ├── main.py
│   ├── picture.py
│   ├── play.py
│   ├── renamer.py
│   ├── reset_watched.py
│   ├── show.py
│   └── watch_input.py
├── server/
│   ├── __init__.py
│   ├── cache.py
│   ├── main.py
│   └── mal.py
├── tests/
│   └── test_config.py
├── pyproject.toml
└── README.md
```

Note: `pyproject.toml` packages only `anime*`; `server/` is not packaged and is run separately.

## Code Conventions

| Item | Standard |
| ---- | -------- |
| Files | snake_case.py |
| User-facing strings | Centralized in `anime/constants.py` |
| Imports | Relative imports inside the package (`from .constants import X`) |
| Local data | Series metadata in `<series>/anime.json` (`{"id": <MAL id>}`); config in platformdirs config dir `directory.json`; covers in platformdirs cache dir `pictures/` |

## Error Patterns

**Propagation:** exceptions are mostly unhandled; HTTP errors use `response.raise_for_status()`; missing VLC raises `RuntimeError(VLC_ERROR)`.

**Logging:** none; user messages via `print`.

## Configuration / Env vars

**Naming:** UPPER_SNAKE_CASE.

**Where declared:** the server reads `MAL_CLIENT_ID` from the environment or `.env` at import time (`server/main.py`); startup fails with KeyError if missing. The CLI resolves the metadata server URL in `anime/config.py` (`get_api_url()` / `resolve_api_url()`), in this order: `ANIME_API_URL` environment variable, `api_url` key in `config.json` (platformdirs config dir, next to `directory.json`; never created by the CLI), default `http://127.0.0.1:8000` (`DEFAULT_API_URL` in `anime/constants.py`). The value is trimmed, trailing `/` removed, and validated (http/https scheme, host, valid port, no credentials). An invalid value or malformed `config.json` raises `ConfigError` with a one-line message and the CLI exits with code 1; there is no fallback to the next source. The URL is only resolved when the interactive menu starts, not for `--rename` or `anime <name> ep<N>`.
