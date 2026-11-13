---
created_at: "2026-11-13 10:46:01"
id: feat-0001-configurable-server-url
n45_version: 1.1.0
title: Configurable server URL
type: feat
---
## As Is

- The metadata server URL is hardcoded as `API_URL = "http://127.0.0.1:8000"` in `anime/constants.py`, and its only use is `AnimeAPI(API_URL)` in `anime/main.py` (interactive menu branch).
- Pointing the CLI at a server on another host or port (NAS, another machine, a different port) requires editing the source.
- User config already lives in `platformdirs.user_config_dir("anime")` (`directory.json` holds the collection directory).

## To Be

The local anime watcher can point the CLI at any metadata server without touching code, via an environment variable or a config file, while the default behavior (`http://127.0.0.1:8000`) stays unchanged for everyone who configures nothing.

## Platform

CLI (curses terminal app).

## Stack

Inherited from STACK, no changes: Python 3.10+, stdlib `os`/`json`/`urllib.parse`, `platformdirs` (already a dependency). Server (`server/`) untouched.
Tests: introduces `pytest` as a dev dependency for unit tests of the URL resolution (the repo currently has no test framework).

## Features / Scope

### Configuration
- Resolve the server URL with precedence: `ANIME_API_URL` env var → `api_url` key in `<user_config_dir>/anime/config.json` → default `http://127.0.0.1:8000`.
- Empty or whitespace-only values are treated as unset (fall through to the next source).
- Strip a trailing `/` from the resolved URL.
- Validation: the URL must have scheme `http` or `https` and a non-empty host. On failure print `Invalid server URL "<value>" (from <source>): must start with http:// or https://` and exit with code 1. `<source>` is `ANIME_API_URL` or the config file path.
- `config.json` that exists but is not valid JSON, or whose `api_url` is not a string → clear error naming the file, exit code 1. Missing file or missing key → fall through to default (the file is not created automatically).
- Resolution happens only where the CLI talks to the server (where `AnimeAPI` is built); `--rename` and direct `anime <name> ep<N>` playback do not read or validate the URL.
- Resolution logic lives in a new small module (`anime/config.py`), following the one-module-per-responsibility pattern; `API_URL` in `constants.py` becomes `DEFAULT_API_URL`, and user-facing messages go to `constants.py`.

### Tests
- `pytest` unit tests for the resolver: env-only, config-only, both (env wins), neither (default), trailing slash, empty values, invalid scheme, malformed JSON, non-string `api_url`.

### Docs
- README: document `ANIME_API_URL` and `config.json` `api_url`.
- Foundational docs update: PATTERNS/RUNBOOK no longer describe the URL as hardcoded; RUNBOOK env var table gains `ANIME_API_URL` (CLI, optional); STACK tests layer gains pytest.

## CLI Configuration Contract

```
Env var
  ANIME_API_URL      — http(s)://host[:port][/path] → overrides everything (optional)

Config file
  <user_config_dir>/anime/config.json
  { "api_url": "http(s)://host[:port][/path]" }   → used when env var unset/empty (optional)

Default
  http://127.0.0.1:8000

Errors (exit 1, message to stderr)
  invalid URL        → Invalid server URL "<value>" (from <source>): must start with http:// or https://
  malformed config   → Invalid config file <path>: <reason>
```

Examples:
- `ANIME_API_URL=http://192.168.1.10:8000 anime` → uses `http://192.168.1.10:8000`
- no env, `config.json` = `{"api_url": "http://nas.local:8000/"}` → uses `http://nas.local:8000`
- nothing set → uses `http://127.0.0.1:8000`
- `ANIME_API_URL=nas.local:8000 anime` → error, exit 1

## Out of Scope

- A `--api-url` CLI flag.
- Changes to the server (`server/`), its port, or its own configuration.
- Friendly handling of an unreachable server (connection errors stay as today).
- Migrating `directory.json` into `config.json` or any other config restructuring.
- An interactive command to edit the config file.

## Dependencies and Impact

- `anime/main.py`: replaces the `API_URL` import with the resolver call.
- `anime/constants.py`: `API_URL` → `DEFAULT_API_URL` + new error messages.
- `pyproject.toml`: optional `dev` extra with `pytest`.
- No impact on the server, the cache, or MyAnimeList integration.
