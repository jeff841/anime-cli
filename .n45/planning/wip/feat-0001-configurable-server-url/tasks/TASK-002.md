---
checkpoint: null
complexity: P
created_at: "2026-11-13 11:07:22"
criteria:
    - done: false
      test: awk '/^## Configuration/{c=NR} /^### Server URL/{s=NR} /^## MyAnimeList API/{m=NR} END{exit !(c && s>c && m>s)}' README.md
      text: README has a '### Server URL' subsection inside '## Configuration' (before '## MyAnimeList API')
    - done: false
      test: grep -qE '^1\. .*ANIME_API_URL' README.md && grep -qE '^2\. .*api_url.*config\.json' README.md && grep -qE '^3\. .*http://127\.0\.0\.1:8000' README.md
      text: README lists the precedence env var -> config.json api_url -> default as a numbered list in that order
    - done: false
      test: 'grep -qF ''export ANIME_API_URL=http://nas.local:8000'' README.md && grep -qE ''"api_url": *"http://nas\.local:8000"'' README.md'
      text: README shows the ANIME_API_URL export example and the config.json JSON example with api_url
    - done: false
      test: grep -qF '~/.config/anime/config.json' README.md && grep -qF 'Library/Application Support/anime/config.json' README.md && grep -qF 'anime\anime\config.json' README.md
      text: README gives the config.json location for Linux, macOS and Windows
    - done: false
      test: 'grep -qF ''exit code 1'' README.md && grep -qF ''Invalid server URL "ftp://x" (from ANIME_API_URL): must start with http:// or https://'' README.md'
      text: 'README documents the error behavior: one stderr line, exit code 1, and the example message'
    - done: false
      test: grep -qF '**Security:**' README.md && grep -qi 'trusted' README.md && grep -qiE 'https.*non-loopback|non-loopback.*https' README.md
      text: README states the configured server is trusted and recommends https for non-loopback hosts
    - done: false
      test: grep -qF 'pip install -e ".[dev]"' README.md && grep -qE '^pytest$' README.md && grep -q '^### Running tests' README.md
      text: README Development section shows how to install the dev extra and run pytest
    - done: false
      test: grep -qE '[├└]── config\.py' README.md && grep -qE '[├└]── constants\.py' README.md && grep -qE '[├└]── test_config\.py' README.md
      text: Project Structure tree lists anime/config.py, anime/constants.py and tests/test_config.py
deps: []
files:
    - README.md
id: TASK-002
n45_version: 1.1.0
outcome: ""
persona: backend
phase: Phase 1 — Configurable server URL
roadmap: feat-0001-configurable-server-url
status: pending
tdd:
    green: false
    red: false
    refactor: false
title: Document server URL configuration and test setup in README
updated_at: "2026-11-13 11:07:22"
---
## Context

`anime-cli` is a terminal anime manager whose curses client fetches MyAnimeList metadata through a small local HTTP server. Until now the client always used the hardcoded server URL `http://127.0.0.1:8000`. A parallel task makes that URL configurable: the CLI now resolves it from the `ANIME_API_URL` environment variable, then from an `api_url` key in an optional `config.json` in the user config directory, then falls back to `http://127.0.0.1:8000`. It also adds `pytest` as a dev-only extra and a test suite under `tests/`.

This task documents that behavior for users and contributors in `README.md` only. It changes no code. The README is the only user-facing documentation of the project; today its "Configuration" section only vaguely describes `directory.json`, and its "Development" section has no test instructions.

Facts to document (they are fixed — do not invent other behavior):

- Env var: `ANIME_API_URL` (e.g. `export ANIME_API_URL=http://nas.local:8000`).
- Config file: `config.json` in the same user configuration directory as the existing `directory.json` (via `platformdirs.user_config_dir("anime")`): `~/.config/anime/config.json` on Linux, `~/Library/Application Support/anime/config.json` on macOS, `%LOCALAPPDATA%\anime\anime\config.json` on Windows. The CLI never creates or modifies this file; the user creates it. Content example: `{ "api_url": "http://nas.local:8000" }`. Unknown keys are ignored.
- Precedence: 1) `ANIME_API_URL`, 2) `api_url` in `config.json`, 3) default `http://127.0.0.1:8000`.
- An empty or whitespace-only value counts as unset and falls through to the next source. Surrounding whitespace and trailing `/` are removed (`http://nas.local:8000/` → `http://nas.local:8000`). A path is allowed (`http://host/api`).
- Validation: the URL must use `http://` or `https://`, have a host, have a valid port if any, and must not contain credentials (`user:password@`).
- Errors: an invalid URL or a malformed `config.json` (unreadable, not UTF-8, invalid JSON, not a JSON object, `api_url` not a string) prints one error line to stderr and the command exits with exit code 1. There is no fallback to the next source when a set value is invalid. Example: `Invalid server URL "ftp://x" (from ANIME_API_URL): must start with http:// or https://`.
- The URL is only read when opening the interactive menu (`anime` / `anime <name>`); `anime --rename` and `anime <name> ep<N>` never read it.
- Security notes: the configured server is trusted — the CLI displays whatever metadata and cover images it returns, so only point it at a server you control. Use `https` for non-loopback hosts (anything other than `127.0.0.1`/`localhost`), because `http` sends requests in clear text over the network.
- Development: `pip install -e ".[dev]"` installs pytest; run `pytest` from the repository root.

## Expected Behavior

| Reader action | What the README provides |
| --- | --- |
| Looks for how to point the CLI at a NAS server | `### Server URL` subsection under `## Configuration` with `export ANIME_API_URL=http://nas.local:8000` example |
| Wants a persistent setting | `config.json` location per OS + JSON example with `"api_url"` |
| Sets both env var and file | numbered precedence list: `1.` env var, `2.` `config.json` `api_url`, `3.` default `http://127.0.0.1:8000` |
| Sets `ANIME_API_URL=ftp://x` | README explains the one-line stderr error and exit code 1, with the example message, and that there is no fallback |
| Puts the server on another machine | README says the configured server is trusted and recommends `https` for non-loopback hosts |
| Contributor wants to run tests | `## Development` shows `pip install -e ".[dev]"` and `pytest` |

## What to Implement

### Files to Create or Modify

| File | Action | Description |
| --- | --- | --- |
| `README.md` | Modify | New `### Server URL` subsection at the end of `## Configuration`; `## Development` gains a "Running tests" part; `## Project Structure` tree gains `config.py`, `constants.py` and `tests/test_config.py` |

### Technical Details

1. Inside `## Configuration` (after the existing text, before `## MyAnimeList API`) add a `### Server URL` subsection containing, in this order:
   1. One sentence: the CLI fetches metadata from a metadata server, by default `http://127.0.0.1:8000`, and it can be changed without editing code.
   2. The precedence as a numbered Markdown list whose lines start at column 0 exactly like:
      ```
      1. `ANIME_API_URL` environment variable
      2. `api_url` key in `config.json`
      3. Default: `http://127.0.0.1:8000`
      ```
   3. A bash block: `export ANIME_API_URL=http://nas.local:8000` then `anime`.
   4. The `config.json` paths per OS (Linux / macOS / Windows, listed above), a JSON block `{ "api_url": "http://nas.local:8000" }`, and the note that the CLI never creates or edits this file.
   5. Normalization and validation rules (blank = unset; whitespace and trailing `/` removed; `http`/`https` only; host required; valid port; no credentials).
   6. Error behavior: one line on stderr, exit code 1, no fallback, with the example message in a `text` block. Write the phrase **`exit code 1`** literally.
   7. The URL is only read for the interactive menu, not for `--rename` or `ep<N>`.
   8. A `> **Security:**` blockquote stating the configured server is **trusted** (word "trusted" literally) and recommending `https` for **non-loopback** hosts (word "non-loopback" literally).
2. In `## Development`, after the editable install, add a `### Running tests` subsection with a bash block containing `pip install -e ".[dev]"` and `pytest` (run from the repository root).
3. In `## Project Structure`, add `config.py` and `constants.py` under `anime/` (alphabetical order with the existing entries) and a `tests/` folder with `test_config.py`.
4. Do not change any other section. Keep the README's existing style (`*` bullets in Features, fenced blocks with language tags).

**Refactoring:** None.
