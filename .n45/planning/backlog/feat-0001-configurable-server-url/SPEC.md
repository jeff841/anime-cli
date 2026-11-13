---
created_at: "2026-11-13 10:52:33"
id: feat-0001-configurable-server-url
n45_version: 1.1.0
status: proposed
title: Configurable metadata server URL
type: feat
updated_at: "2026-11-13 10:52:33"
---
## 1. Overview

**Goal (To Be):** The local anime watcher can point the CLI at any metadata server (another host, port or path) through the `ANIME_API_URL` environment variable or an `api_url` key in the user config file, without editing code; with nothing configured the CLI keeps using `http://127.0.0.1:8000`.

**Work shape:** `build`

**Background (As Is):** The metadata server URL is hardcoded as `API_URL = "http://127.0.0.1:8000"` in `anime/constants.py`; its only consumer is `AnimeAPI(API_URL)` in the interactive-menu branch of `anime/main.py`. Running the server on a NAS, another machine or another port requires editing the source. User config already lives in `platformdirs.user_config_dir("anime")` (holds `directory.json`). The repository has no test framework.

### Functional Requirements

- **RF-01** — The CLI must resolve the server URL with the precedence `ANIME_API_URL` env var → `api_url` key in `<user_config_dir("anime")>/config.json` → default `http://127.0.0.1:8000`.
- **RF-02** — An empty or whitespace-only value (env var or `api_url`) must be treated as unset and fall through to the next source; non-empty values are used with surrounding whitespace stripped and all trailing `/` removed.
- **RF-03** — The resolved URL must be validated with `urllib.parse.urlsplit`: scheme exactly `http` or `https` (case-insensitive), non-empty host, no userinfo (username/password), parseable port. Any violation is fail-closed: one-line message on stderr, exit code 1, no traceback, no fallback to another source.
- **RF-04** — A `config.json` that exists but cannot be read, is not UTF-8, is not valid JSON, has a non-object top level, or has an `api_url` that is present but not a string must produce one clear error naming the file on stderr, exit code 1, no traceback. A missing file or missing `api_url` key falls through to the default.
- **RF-05** — Every value echoed in an error message (URL, config path, JSON reason) must have non-printable characters (control chars, ANSI escape `\x1b`, newline) neutralized as `\xNN`/`\uNNNN` escapes, and a URL with userinfo must never have its credentials printed.
- **RF-06** — The resolver must have no filesystem side effects (never creates, writes or modifies `config.json` or its directory) and read no source other than the env var, `config.json` and the default.
- **RF-07** — Resolution happens only in the interactive-menu branch of `main()` (where `AnimeAPI` is built); `anime --rename [...]` and `anime <name> ep<N>` never read or validate the URL.
- **RF-08** — `pytest` is available as a dev-only extra and unit tests cover every resolution path, error path and hostile input listed in §8.
- **RF-09** — The README documents `ANIME_API_URL`, `config.json` `api_url`, precedence, error behavior, that the configured server is trusted, and that `https` is recommended for non-loopback hosts.
- **RF-10** — Foundational docs no longer describe the URL as hardcoded: PATTERNS (client/server split + configuration section), RUNBOOK (env var table gains `ANIME_API_URL`, CLI, optional, default `http://127.0.0.1:8000`), STACK (tests layer = pytest).

## 2. Technology Stack

Only changes (existing project):

| Layer | Component | Technology | Note |
| ----- | --------- | ---------- | ---- |
| tests | Unit tests | `pytest>=7` | Dev-only extra `[project.optional-dependencies] dev`; not a runtime dependency |
| backend (CLI) | URL resolution | stdlib `os`, `json`, `urllib.parse`, `sys`, `pathlib` + `platformdirs` (already a dependency) | No new runtime dependency |

The server (`server/`) is untouched.

## 3. Data Modeling

No database change. New optional user file (never created by the CLI):

`<platformdirs.user_config_dir("anime")>/config.json` — same directory as the existing `directory.json` (e.g. `~/.config/anime/config.json` on Linux).

```json
{ "api_url": "http://nas.local:8000" }
```

- Top level: JSON object. Unknown keys are ignored.
- `api_url`: optional string. Absent → default. Empty/whitespace → default. Non-string (including `null`, number, object) → error (RF-04).
- `directory.json` is not touched or merged.

## 4. Contracts and Architecture

### Interfaces

New module `anime/config.py` (one module per responsibility, plain functions; relative imports):

```python
# anime/config.py
from collections.abc import Mapping
from pathlib import Path


class ConfigError(Exception):
    """Raised with an already-formatted, safe, one-line user message."""


def config_file_path() -> Path:
    """Return Path(user_config_dir(CONFIG)) / CONFIG_JSON. Never creates anything."""


def resolve_api_url(
    environ: Mapping[str, str] | None = None,   # None -> os.environ
    config_file: Path | None = None,            # None -> config_file_path()
) -> str:
    """Return the validated server URL without trailing '/'.

    Precedence: environ[API_URL_ENV] -> config_file[API_URL_KEY] -> DEFAULT_API_URL.
    Raises ConfigError (message already formatted and sanitized) on invalid URL or
    malformed config file. Pure: no writes, no prints, no sys.exit.
    The config file is only opened when the env var is unset/empty.
    """


def get_api_url() -> str:
    """CLI entry: return resolve_api_url(); on ConfigError print the message to
    sys.stderr and raise SystemExit(1). No traceback."""
```

Constants added to `anime/constants.py` (user-facing strings centralized; `API_URL` removed and replaced):

```python
DEFAULT_API_URL = "http://127.0.0.1:8000"
API_URL_ENV = "ANIME_API_URL"
API_URL_KEY = "api_url"
CONFIG_JSON = "config.json"
INVALID_URL = 'Invalid server URL "{value}" (from {source}): {reason}'
URL_BAD_SCHEME = "must start with http:// or https://"
URL_NO_HOST = "missing host"
URL_CREDENTIALS = "must not contain credentials"
URL_BAD_PORT = "invalid port"
INVALID_CONFIG = "Invalid config file {path}: {reason}"
CONFIG_UNREADABLE = "cannot be read ({error})"
CONFIG_NOT_UTF8 = "not valid UTF-8"
CONFIG_BAD_JSON = "not valid JSON ({error})"
CONFIG_NOT_OBJECT = "top-level value must be a JSON object"
CONFIG_URL_NOT_STRING = '"api_url" must be a string'
```

**Validation algorithm (contract, in this order):**

1. `value = raw.strip()`; empty → source is unset (fall through).
2. `parts = urlsplit(value)`.
3. `parts.scheme.lower() not in {"http", "https"}` → `URL_BAD_SCHEME`. (Covers `file://`, `ftp://`, `javascript:`, `nas.local:8000`, missing scheme.) Allow-list on the parsed scheme only — never prefix/substring matching.
4. `parts.username is not None or parts.password is not None` → `URL_CREDENTIALS`.
5. `not parts.hostname` → `URL_NO_HOST`.
6. Accessing `parts.port` raises `ValueError` → `URL_BAD_PORT`.
7. Return `value.rstrip("/")` (an `http://host/` becomes `http://host`; path preserved: `http://host/api/` → `http://host/api`).

**Error-message contract:**

- `{source}` = `ANIME_API_URL` for the env var, or the config file path (`str(path)`) for the file.
- `{value}` = the stripped raw value, sanitized (RF-05). For `URL_CREDENTIALS`, `{value}` is the URL rebuilt without userinfo and with `***@` in its place (e.g. `http://***@nas.local:8000`) — the username and password never appear.
- Sanitization helper (private, in `anime/config.py`): every character for which `str.isprintable()` is False is replaced by its escape (`\x1b`, `\n`, `​`...); printable characters, including non-ASCII letters, are kept. Applied to `{value}`, `{source}`, `{path}` and the `{error}` text.
- `CONFIG_BAD_JSON` `{error}` = `f"line {e.lineno} column {e.colno}"` from `JSONDecodeError` (not the full message, which can echo file content). `RecursionError` from deeply nested JSON is reported as `CONFIG_BAD_JSON` with `{error}` = `"nesting too deep"`.
- `CONFIG_UNREADABLE` `{error}` = `e.strerror or type(e).__name__` from `OSError` (e.g. permission denied, path is a directory).

**Config file read (contract):** `config_file.read_bytes()` → `FileNotFoundError` = absent (fall through); other `OSError` → `CONFIG_UNREADABLE`; `.decode("utf-8")` failure → `CONFIG_NOT_UTF8`; `json.loads` → `JSONDecodeError`/`RecursionError` → `CONFIG_BAD_JSON`; not `dict` → `CONFIG_NOT_OBJECT`; `api_url` key absent → fall through; present and not `str` → `CONFIG_URL_NOT_STRING`; string → steps 1-7 with source = file path. An empty (0-byte) file is invalid JSON → error.

**Invalid set source never falls back:** if the env var is set (non-empty) and invalid, the CLI exits — it does not try the config file or default. Same for an invalid `api_url`.

### Data Flow

`main()` (interactive-menu branch) → `get_api_url()` → `resolve_api_url(os.environ, config_file_path())` → `AnimeAPI(url)` → httpx calls `{url}/anime/search`, `{url}/anime/{id}`. Synchronous, once per entry into that branch (the `Exit` → `main()` recursion re-resolves, which is deterministic and cheap).

`main.py` change (interactive branch): the API client is built **before** `watch_input(...)`, so a bad URL fails immediately on stdout/stderr before any curses screen opens:

```python
    else:
        api = AnimeAPI(get_api_url())
        anime = watch_input(args.anime_name)
        items = None
        picture = None
        if anime is None:
            return
        ...
```

The `--rename` and `ep<N>` branches are unchanged and never call `get_api_url()`.

### Impact on Existing Files

| File / Module | Change | Note |
| ------------- | ------ | ---- |
| `anime/config.py` | **New** — `ConfigError`, `config_file_path`, `resolve_api_url`, `get_api_url`, private sanitize/validate helpers | No filesystem writes |
| `anime/constants.py` | `API_URL` removed → `DEFAULT_API_URL`; new constants listed above | `API_URL` must not remain anywhere in `anime/` |
| `anime/main.py` | Import `get_api_url` from `.config`; drop `API_URL` import; `api = AnimeAPI(get_api_url())` moved to the first line of the interactive branch | Other branches untouched |
| `anime/api.py` | None | Receives the URL already without trailing `/` |
| `pyproject.toml` | Add `[project.optional-dependencies] dev = ["pytest>=7"]` and `[tool.pytest.ini_options] testpaths = ["tests"]`, `pythonpath = ["."]` | Runtime `dependencies` unchanged |
| `tests/test_config.py` | **New** — pytest unit tests (uses `tmp_path`, injected `environ` dict, `capsys`) | Never touches the real user config dir |
| `README.md` | New "Server URL" subsection under Configuration; Development section gains `pip install -e ".[dev]"` and `pytest` | |
| PATTERNS / RUNBOOK / STACK | Updated per RF-10 through the N45 docs flow | Not edited directly |

## 6. Boundaries

**In scope:**

- `ANIME_API_URL` env var and `config.json` `api_url` resolution with validation and safe errors.
- `pytest` dev extra and resolver unit tests.
- README and foundational docs updates.

**Out of scope:**

- A `--api-url` CLI flag.
- Any change to `server/`, its port or its configuration.
- Friendly handling of an unreachable server (connection errors stay as today).
- Migrating `directory.json` into `config.json`, auto-creating `config.json`, or an interactive config editor.
- Warning on `http` to a non-loopback host (documented recommendation only).
- Follow-ups (recorded, not done here): timeout and size cap on the cover image download in `anime/picture.py` (server-supplied `main_picture.large`); stripping control characters from server-supplied text before curses rendering.

## 7. Constraints

- No new runtime dependency; `pytest` is dev-only.
- `resolve_api_url` is pure (no print, no exit, no writes) and accepts injected `environ`/`config_file` so tests never read the real environment or user config dir.
- Scheme check is an allow-list on `urlsplit(...).scheme` — no `startswith`/substring checks.
- No traceback is ever shown for configuration errors: only `ConfigError` is caught in `get_api_url`, and every expected failure in the resolver is converted to `ConfigError`.
- All user-facing strings live in `anime/constants.py`; relative imports inside the package.
- Default behavior with nothing configured is byte-for-byte the same URL as today (`http://127.0.0.1:8000`).

## 8. Acceptance Criteria

### RF-01

- [ ] `resolve_api_url({"ANIME_API_URL": "http://192.168.1.10:8000"}, missing_path)` returns `http://192.168.1.10:8000`.
- [ ] With env empty and `config.json` = `{"api_url": "http://nas.local:8000"}`, returns `http://nas.local:8000`.
- [ ] With both set, the env var wins and the config file is not consulted (a malformed config file does not raise when the env var is valid).
- [ ] With neither set (no env var, file absent), returns `http://127.0.0.1:8000`.
- [ ] `config_file_path()` equals `Path(user_config_dir("anime")) / "config.json"`.

### RF-02

- [ ] `ANIME_API_URL=""` and `ANIME_API_URL="   "` fall through to the config file / default.
- [ ] `{"api_url": ""}` and `{"api_url": "  "}` fall through to the default.
- [ ] `"http://nas.local:8000/"` → `http://nas.local:8000`; `"http://host/api//"` → `http://host/api`; `"  http://host:9000  "` → `http://host:9000`.

### RF-03

- [ ] `nas.local:8000`, `file:///etc/passwd`, `ftp://host`, `javascript:alert(1)` each raise `ConfigError` whose message contains `must start with http:// or https://` and the source.
- [ ] `HTTPS://Host:8443` is accepted.
- [ ] `http://` and `http:///path` raise `ConfigError` with `missing host`.
- [ ] `http://host:abc` raises `ConfigError` with `invalid port`.
- [ ] An invalid env var with a valid config file still raises (no fallback).
- [ ] `get_api_url()` with an invalid value writes exactly one line to stderr, nothing to stdout, and raises `SystemExit` with code 1 (verified with `capsys` + `pytest.raises(SystemExit)`).

### RF-04

- [ ] File with `{bad json` → `ConfigError` starting with `Invalid config file <path>: not valid JSON (line`.
- [ ] 0-byte file → `not valid JSON`.
- [ ] File with bytes `b"\xff\xfe"` → `not valid UTF-8`.
- [ ] File containing `[]` → `top-level value must be a JSON object`.
- [ ] `{"api_url": 8000}` and `{"api_url": null}` → `"api_url" must be a string`.
- [ ] Path that is a directory → `cannot be read (`.
- [ ] `{"other": 1}` (key absent) → default URL.
- [ ] Invalid `api_url` value in the file → message has `(from <config path>)`.

### RF-05

- [ ] `http://user:secret@host` raises `ConfigError` with `must not contain credentials`; the message contains neither `user` nor `secret` and contains `***@host`.
- [ ] A value containing `\x1b[31m` and `\n` produces a message with the literal text `\x1b` and `\n` escapes and no actual ESC or newline character.
- [ ] Non-ASCII printable characters (e.g. `é`) are kept as-is in messages.

### RF-06

- [ ] Calling `resolve_api_url` with a `config_file` in a non-existent directory under `tmp_path` leaves that directory non-existent afterwards.
- [ ] `grep -nE "write_text|write_bytes|mkdir|touch|\.open\(|[^_]open\(" anime/config.py` finds nothing (the file is read only via `read_bytes()`; the error is printed with `print(..., file=sys.stderr)`).

### RF-07

- [ ] `grep -n "get_api_url" anime/main.py` shows exactly one call site, inside the final `else:` (interactive) branch, before `watch_input`.
- [ ] `grep -rn "API_URL\b" anime/ | grep -v "DEFAULT_API_URL\|API_URL_ENV\|API_URL_KEY"` returns nothing.
- [ ] With `ANIME_API_URL=bad` exported, `anime --rename <dir>` and `anime <name> ep<N>` behave as before (the URL is not read).

### RF-08

- [ ] `pyproject.toml` has `dev = ["pytest>=7"]` under `[project.optional-dependencies]`, and `pytest` is absent from `[project] dependencies`.
- [ ] `pip install -e ".[dev]" && pytest` passes from the repo root, and `tests/test_config.py` contains tests for every criterion of RF-01..RF-06.

### RF-09

- [ ] README contains `ANIME_API_URL`, `config.json`, `api_url`, the precedence order env → file → default, the default `http://127.0.0.1:8000`, the exit-1 error behavior, a statement that the configured server is trusted, and the recommendation of `https` for non-loopback hosts.

### RF-10

- [ ] PATTERNS no longer says the server URL is hardcoded; RUNBOOK env var table lists `ANIME_API_URL` (CLI, optional, default `http://127.0.0.1:8000`); STACK tests layer lists `pytest`.

## 9. Quality Gates

- `pytest` green from the repo root.
- Every branch of `anime/config.py` (each fall-through, each error reason, success path) is exercised by at least one test — enforced by the RF-08 criterion rather than a coverage tool (no `pytest-cov` dependency).

## 10. Decisions and Trade-offs

| Decision | Discarded alternative | Justification |
| -------- | --------------------- | ------------- |
| Error template `Invalid server URL "<value>" (from <source>): <reason>` with distinct reasons (bad scheme / missing host / credentials / invalid port) | Discovery's single reason "must start with http:// or https://" for every failure | `http://` or `http://user:pw@host` already start with `http://`; the single reason would be wrong for them. The scheme case keeps the exact Discovery wording. |
| Pure `resolve_api_url` raising `ConfigError` + thin `get_api_url` doing print/exit | Resolver printing and calling `sys.exit` directly | Testable without patching `sys.exit`, guarantees no traceback in one place, keeps side effects out of the resolver (RF-06). |
| Build `AnimeAPI` at the start of the interactive branch (before `watch_input`) | Keep it after `watch_input` where it is today | A bad URL is reported before curses menus and before the user picks a series; still lazy relative to `--rename`/`ep<N>`. |
| Reject URLs with userinfo | Accept and only redact in messages (security's minimum) | The server needs no auth; credentials in an env var/URL leak via process lists; rejecting is simpler and fail-closed. |
| No warning for `http` to non-loopback hosts | One-time stderr warning (security's optional suggestion) | LAN/NAS over http is the feature's main use case; a recurring warning before curses is noise. README recommendation covers it. |
| Config path is fixed (`platformdirs`) with no containment check | Verify the file resolves inside the config dir (security: "must not follow a path outside that dir") | No user-controlled path component exists; the file holds no secrets; per-user dir permissions are the boundary. |
| No coverage tool; branch coverage enforced by explicit AC list | Add `pytest-cov` and gate at ≥80% | Security asked for `pytest` as the only dev addition; the module is small and every branch is enumerated in §8. |
| Error on `"api_url": null` | Treat `null` as unset | Discovery says non-string → error; explicit is safer than silently defaulting. |

## 11. Ambiguity Report

| Dimension | Score | Min | Status | Notes |
| --------- | ----- | --- | ------ | ----- |
| Goal Clarity | 0.95 | 0.75 | ok | Precedence, default and contract fixed in Discovery |
| Boundary Clarity | 0.90 | 0.70 | ok | Out-of-scope and follow-ups explicit |
| Constraint Clarity | 0.90 | 0.65 | ok | Pure resolver, no runtime deps, allow-list parsing |
| Acceptance Criteria | 0.90 | 0.70 | ok | Every RF has pass/fail criteria with concrete inputs |
| **Ambiguity** | 0.09 | ≤0.20 | ok | |
