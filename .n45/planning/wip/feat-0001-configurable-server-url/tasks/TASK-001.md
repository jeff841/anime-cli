---
checkpoint: null
complexity: M
created_at: "2026-11-13 11:06:37"
criteria:
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_env_var_wins or test_env_var_skips_malformed_config'
      text: 'Env var wins: ANIME_API_URL=http://192.168.1.10:8000 is returned unchanged, and a malformed config.json is not read when the env var is valid'
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_config_file_used_when_env_unset or test_blank_env_falls_through or test_blank_api_url_falls_back_to_default'
      text: config.json api_url http://nas.local:8000 is used when the env var is unset, blank ('' / '   ') env falls through, blank api_url falls back to the default
    - done: false
      test: python -c "from pathlib import Path; from anime.config import resolve_api_url; assert resolve_api_url({}, Path('/nonexistent-n45-dir/config.json')) == 'http://127.0.0.1:8000'" && python -m pytest tests/test_config.py -q -k test_default_when_nothing_configured
      text: With nothing configured resolve_api_url returns exactly http://127.0.0.1:8000
    - done: false
      test: 'python -c "from pathlib import Path; from anime.config import resolve_api_url as r; m = Path(''/nonexistent-n45-dir/config.json''); assert r({''ANIME_API_URL'': ''http://host/api//''}, m) == ''http://host/api''; assert r({''ANIME_API_URL'': ''  http://host:9000  ''}, m) == ''http://host:9000''; assert r({''ANIME_API_URL'': ''http://nas.local:8000/''}, m) == ''http://nas.local:8000''" && python -m pytest tests/test_config.py -q -k test_url_normalization'
      text: 'Normalization strips whitespace and every trailing slash: ''http://host/api//'' -> ''http://host/api'', ''  http://host:9000  '' -> ''http://host:9000'''
    - done: false
      test: python -c "from pathlib import Path; from platformdirs import user_config_dir; from anime.config import config_file_path; assert config_file_path() == Path(user_config_dir('anime')) / 'config.json'" && python -m pytest tests/test_config.py -q -k test_config_file_path_location
      text: config_file_path() equals Path(user_config_dir('anime')) / 'config.json'
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_bad_scheme_rejected or test_uppercase_https_accepted'
      text: nas.local:8000, file:///etc/passwd, ftp://host and javascript:alert(1) are rejected with 'must start with http:// or https://' naming the source, while HTTPS://Host:8443 is accepted
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_missing_host_rejected or test_invalid_port_rejected or test_malformed_url_rejected'
      text: http:// and http:///path raise 'missing host', http://host:abc raises 'invalid port', and a value urlsplit cannot parse (http://[::1) raises 'malformed URL' instead of a traceback
    - done: false
      test: |-
        python -c "from pathlib import Path; from anime.config import resolve_api_url, ConfigError
        try:
            resolve_api_url({'ANIME_API_URL': 'http://[::1'}, Path('/nonexistent-n45-dir/config.json'))
        except ConfigError as e:
            assert str(e).endswith(': malformed URL'), str(e)
        else:
            raise SystemExit('no error raised')"
      text: Malformed IPv6-like value is converted to ConfigError (no bare ValueError escapes)
    - done: false
      test: python -m pytest tests/test_config.py -q -k test_invalid_env_does_not_fall_back
      text: An invalid env var with a valid config.json still raises (no fallback)
    - done: false
      test: 'python -m pytest tests/test_config.py -q -k ''test_get_api_url_exits_1_with_one_stderr_line or test_get_api_url_returns_resolved_url'' && err=$(ANIME_API_URL=ftp://x python -c ''from anime.config import get_api_url; get_api_url()'' 2>&1 >/dev/null); rc=$?; test $rc -eq 1 && test "$err" = ''Invalid server URL "ftp://x" (from ANIME_API_URL): must start with http:// or https://'''
      text: get_api_url() with an invalid ANIME_API_URL writes exactly one stderr line, no stdout, exits with code 1 and no traceback
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_config_bad_json or test_config_empty_file or test_config_not_utf8 or test_config_not_object or test_config_api_url_not_string or test_config_path_is_directory or test_config_deeply_nested_json or test_config_invalid_url_names_file'
      text: 'Malformed config.json cases produce ''Invalid config file <path>: <reason>'' (bad JSON with line/column, empty file, non-UTF-8, non-object, non-string api_url incl. null, directory path, nesting too deep) and an invalid api_url names the file as source'
    - done: false
      test: python -m pytest tests/test_config.py -q -k test_config_key_absent_returns_default
      text: 'config.json without api_url ({"other": 1}) returns the default URL'
    - done: false
      test: |-
        python -c "from pathlib import Path; from anime.config import resolve_api_url, ConfigError
        try:
            resolve_api_url({'ANIME_API_URL': 'http://user:secret@host'}, Path('/nonexistent-n45-dir/config.json'))
        except ConfigError as e:
            m = str(e); assert '***@host' in m and 'user' not in m and 'secret' not in m and 'must not contain credentials' in m, m
        else:
            raise SystemExit('no error raised')" && python -m pytest tests/test_config.py -q -k test_credentials_rejected_and_redacted
      text: http://user:secret@host is rejected with 'must not contain credentials' and the message shows http://***@host without 'user' or 'secret'
    - done: false
      test: python -m pytest tests/test_config.py -q -k 'test_control_chars_escaped or test_non_ascii_kept'
      text: Control characters in echoed values become literal escapes (\x1b, \n) with no real ESC/newline in the message, and printable non-ASCII (café) is kept
    - done: false
      test: python -m pytest tests/test_config.py -q -k test_resolver_creates_nothing && ! grep -nE 'write_text|write_bytes|mkdir|touch|\.open\(|[^_]open\(' anime/config.py
      text: 'The resolver has no filesystem side effects: a config_file in a non-existent tmp dir leaves the dir non-existent, and config.py has no write/mkdir/touch/open calls'
    - done: false
      test: test "$(grep -c 'get_api_url()' anime/main.py)" -eq 1 && awk '/^    else:/{e=NR} /AnimeAPI\(get_api_url\(\)\)/{a=NR} /watch_input\(args\.anime_name\)/{w=NR} END{exit !(e && a>e && w>a)}' anime/main.py
      text: 'main.py calls get_api_url() exactly once, as AnimeAPI(get_api_url()) inside the final interactive else: branch before watch_input'
    - done: false
      test: '! grep -nw ''API_URL'' anime/main.py anime/constants.py anime/config.py'
      text: The name API_URL no longer exists in the package (only DEFAULT_API_URL / API_URL_ENV / API_URL_KEY)
    - done: false
      test: python -c 'import anime.main' && test "$(grep -c 'AnimeAPI(' anime/main.py)" -eq 1
      text: '--rename and ep<N> branches never resolve the URL: main.py still imports cleanly and AnimeAPI is only built in the interactive branch'
    - done: false
      test: grep -qE '^dev = \["pytest>=7"\]' pyproject.toml && grep -qF 'testpaths = ["tests"]' pyproject.toml && grep -qF 'pythonpath = ["."]' pyproject.toml && ! sed -n '/^dependencies/,/^\]/p' pyproject.toml | grep -q pytest
      text: pyproject.toml declares pytest only as the dev extra and configures testpaths/pythonpath
    - done: false
      test: '! grep -nE ''pytest\.raises\(ConfigError\):'' tests/test_config.py'
      text: 'Every ConfigError expectation checks the message: no bare ''with pytest.raises(ConfigError):'' in the suite'
    - done: false
      test: python -m pytest -q
      text: Whole suite passes from the repo root
deps: []
files:
    - anime/config.py
    - anime/constants.py
    - anime/main.py
    - tests/test_config.py
    - pyproject.toml
    - .gitignore
id: TASK-001
linter: python -m py_compile anime/config.py anime/constants.py anime/main.py tests/test_config.py
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
tests: python -m pytest tests/test_config.py -q
title: Resolve server URL from ANIME_API_URL / config.json with validation and pytest suite
updated_at: "2026-11-13 11:06:37"
---
## Context

`anime-cli` is a Python 3.10+ curses CLI (`anime/` package) that talks to a small local FastAPI metadata server (`server/`, untouched by this task). Today the server URL is hardcoded as `API_URL = "http://127.0.0.1:8000"` in `anime/constants.py`, and its only consumer is `AnimeAPI(API_URL)` in the interactive-menu branch of `main()` in `anime/main.py`. Running the server on a NAS, another machine or another port therefore requires editing source code.

This task makes the URL configurable without code edits. The CLI resolves it with the precedence **`ANIME_API_URL` env var → `api_url` key in `<platformdirs.user_config_dir("anime")>/config.json` → default `http://127.0.0.1:8000`**, validates it fail-closed, prints safe one-line errors (exit code 1, never a traceback), and has no filesystem side effects. With nothing configured the URL must be byte-for-byte the same as today (`http://127.0.0.1:8000`).

The repository has no test framework yet: this task also adds `pytest` as a **dev-only** extra and the first test suite (`tests/test_config.py`). `server/`, `anime/api.py` and every other module stay untouched. No new runtime dependency (`platformdirs` is already one).

Project conventions you must follow:

- One small module per responsibility, plain functions; one class only when needed (here: the exception).
- snake_case modules/functions, PascalCase classes, UPPER_SNAKE constants.
- **All user-facing strings live in `anime/constants.py`**; inside the package use relative imports (`from .constants import X`).
- The existing user config dir is `Path(user_config_dir(CONFIG))` with `CONFIG = "anime"` (already in `anime/constants.py`; `anime/watch_input.py` uses it for `directory.json`). `config.json` lives in that same directory; `directory.json` is never touched or merged.
- No logging framework; user messages via `print`.

## Expected Behavior

`resolve_api_url(environ, config_file)` is **pure**: no print, no `sys.exit`, no writes. It returns the validated URL or raises `ConfigError` whose `str()` is the final, already sanitized, one-line user message. `get_api_url()` is the thin CLI entry: on `ConfigError` it prints the message to `sys.stderr` and raises `SystemExit(1)`.

`missing` below = a path that does not exist (e.g. `tmp_path / "nope" / "config.json"`). `cfg(x)` = a `config.json` under `tmp_path` written with content `x`. `P` = `str(path)` of that config file.

| Input / Action | Expected output / effect |
| --- | --- |
| `resolve_api_url({"ANIME_API_URL": "http://192.168.1.10:8000"}, missing)` | `"http://192.168.1.10:8000"` |
| `resolve_api_url({}, cfg('{"api_url": "http://nas.local:8000"}'))` | `"http://nas.local:8000"` |
| `resolve_api_url({"ANIME_API_URL": "http://192.168.1.10:8000"}, cfg('{bad json'))` | `"http://192.168.1.10:8000"` (config file is never opened when the env var is non-empty) |
| `resolve_api_url({}, missing)` | `"http://127.0.0.1:8000"` |
| `config_file_path()` | `Path(user_config_dir("anime")) / "config.json"` (nothing created) |
| `resolve_api_url({"ANIME_API_URL": ""}, cfg('{"api_url": "http://nas.local:8000"}'))` and same with `"   "` | `"http://nas.local:8000"` (blank env = unset) |
| `resolve_api_url({}, cfg('{"api_url": ""}'))` and `'{"api_url": "  "}'` | `"http://127.0.0.1:8000"` |
| env `"http://nas.local:8000/"` | `"http://nas.local:8000"` |
| env `"http://host/api//"` | `"http://host/api"` |
| env `"  http://host:9000  "` | `"http://host:9000"` |
| env `"HTTPS://Host:8443"` | `"HTTPS://Host:8443"` (accepted; scheme compare is case-insensitive, value returned unchanged apart from strip/trailing `/`) |
| env `"nas.local:8000"`, `"file:///etc/passwd"`, `"ftp://host"`, `"javascript:alert(1)"` | `ConfigError`: `Invalid server URL "<value>" (from ANIME_API_URL): must start with http:// or https://` — e.g. `Invalid server URL "ftp://host" (from ANIME_API_URL): must start with http:// or https://` |
| env `"http://"` and `"http:///path"` | `ConfigError` ending in `: missing host` |
| env `"http://host:abc"` | `ConfigError`: `Invalid server URL "http://host:abc" (from ANIME_API_URL): invalid port` |
| env `"ftp://x"` + `cfg('{"api_url": "http://nas.local:8000"}')` | `ConfigError` (`must start with http:// or https://`) — **no fallback** to file or default |
| env `"http://user:secret@host"` | `ConfigError`: `Invalid server URL "http://***@host" (from ANIME_API_URL): must not contain credentials` — message contains neither `user` nor `secret` |
| env `"ftp://ho\nst\x1b[31m"` (Python literal: real newline + real ESC inside the value) | `ConfigError` whose message is `Invalid server URL "ftp://ho\nst\x1b[31m" (from ANIME_API_URL): malformed URL` where `\n` and `\x1b` are **literal backslash escapes**; the message contains **no** real ESC character and **no** real newline (`urlsplit` raises `ValueError: Invalid IPv6 URL` here because of the `[`) |
| env `"http://[::1"` | `ConfigError` ending in `: malformed URL` (`urlsplit` itself raises `ValueError`) |
| env `"ftp://café"` | message contains `café` unchanged (printable non-ASCII is kept) |
| `cfg('{bad json')` (env unset) | `ConfigError` starting with `Invalid config file P: not valid JSON (line` — exactly `Invalid config file P: not valid JSON (line 1 column 2)` |
| `cfg('')` (0-byte file) | `Invalid config file P: not valid JSON (line 1 column 1)` |
| config file containing raw bytes `b"\xff\xfe"` | `Invalid config file P: not valid UTF-8` |
| `cfg('[]')` | `Invalid config file P: top-level value must be a JSON object` |
| `cfg('{"api_url": 8000}')` and `cfg('{"api_url": null}')` | `Invalid config file P: "api_url" must be a string` |
| `config_file` is a directory (`tmp_path` itself) | message starts with `Invalid config file P: cannot be read (` (e.g. `cannot be read (Is a directory)`) |
| `cfg('[' * 100000)` | `Invalid config file P: not valid JSON (nesting too deep)` |
| `cfg('{"other": 1}')` | `"http://127.0.0.1:8000"` |
| `cfg('{"api_url": "ftp://x"}')` | `Invalid server URL "ftp://x" (from P): must start with http:// or https://` |
| `resolve_api_url({}, tmp_path / "newdir" / "config.json")` | returns default; `tmp_path / "newdir"` still does **not** exist afterwards |
| `get_api_url()` with `ANIME_API_URL=ftp://x` (monkeypatched env) | exactly one line on stderr (the message), nothing on stdout, `SystemExit` with `code == 1`, no traceback |
| `get_api_url()` with `ANIME_API_URL=http://nas.local:8000/` | returns `"http://nas.local:8000"` |

`main()` behavior:

| Action | Effect |
| --- | --- |
| `anime` (interactive menu) with `ANIME_API_URL=bad` | error line on stderr + exit 1 **before** `watch_input` / any curses screen |
| `anime --rename <dir>` or `anime <name> ep<N>` with `ANIME_API_URL=bad` | unchanged behavior; the URL is never read or validated |

## TDD

Write `tests/test_config.py` first (red), then implement (green). Tests must **never** read the real environment or the real user config dir: always pass an explicit `environ` dict and a `config_file` under `tmp_path` to `resolve_api_url`; for `get_api_url()` use `monkeypatch.setenv("ANIME_API_URL", ...)` (env is non-empty so the config file is never opened). Import as `from anime.config import ConfigError, config_file_path, get_api_url, resolve_api_url`.

Two exemplary tests (fix the assertion style — exact values, message checked, not just the exception type):

```python
import pytest
from pathlib import Path

from anime.config import ConfigError, get_api_url, resolve_api_url


def test_invalid_env_does_not_fall_back(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text('{"api_url": "http://nas.local:8000"}', encoding="utf-8")
    with pytest.raises(ConfigError) as excinfo:
        resolve_api_url({"ANIME_API_URL": "ftp://x"}, cfg)
    assert str(excinfo.value) == (
        'Invalid server URL "ftp://x" (from ANIME_API_URL): '
        "must start with http:// or https://"
    )


def test_get_api_url_exits_1_with_one_stderr_line(monkeypatch, capsys):
    monkeypatch.setenv("ANIME_API_URL", "ftp://x")
    with pytest.raises(SystemExit) as excinfo:
        get_api_url()
    assert excinfo.value.code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err == (
        'Invalid server URL "ftp://x" (from ANIME_API_URL): '
        "must start with http:// or https://\n"
    )
```

Cover every remaining row of the tables above. **Use exactly these test names** (the acceptance criteria select them with `pytest -k`; `pytest.mark.parametrize` is welcome for the multi-value rows):

- `test_env_var_wins`, `test_env_var_skips_malformed_config`, `test_config_file_used_when_env_unset`, `test_default_when_nothing_configured`, `test_config_file_path_location`
- `test_blank_env_falls_through`, `test_blank_api_url_falls_back_to_default`, `test_url_normalization`
- `test_bad_scheme_rejected`, `test_uppercase_https_accepted`, `test_missing_host_rejected`, `test_invalid_port_rejected`, `test_malformed_url_rejected`, `test_invalid_env_does_not_fall_back`, `test_get_api_url_exits_1_with_one_stderr_line`, `test_get_api_url_returns_resolved_url`
- `test_config_bad_json`, `test_config_empty_file`, `test_config_not_utf8`, `test_config_not_object`, `test_config_api_url_not_string`, `test_config_path_is_directory`, `test_config_deeply_nested_json`, `test_config_key_absent_returns_default`, `test_config_invalid_url_names_file`
- `test_credentials_rejected_and_redacted` (use the env var as source — a `tmp_path` path can contain the OS user name), `test_control_chars_escaped`, `test_non_ascii_kept`
- `test_resolver_creates_nothing`

Every `pytest.raises(ConfigError)` must capture the exception (`as excinfo`) or use `match=` and assert on the message text — a bare `with pytest.raises(ConfigError):` passes with the wrong reason and is forbidden. For the control-char test assert both directions: `"\\x1b" in msg and "\\n" in msg` **and** `"\x1b" not in msg and "\n" not in msg`.

**Refactoring:** after green, collapse repeated "write config file" boilerplate into a small local helper/fixture in the test module; keep `anime/config.py` free of duplicated message formatting (one helper builds the `INVALID_URL` message).

## What to Implement

### Files to Create or Modify

| File | Action | Description |
| --- | --- | --- |
| `anime/config.py` | Create | `ConfigError`, `config_file_path`, `resolve_api_url`, `get_api_url`, private `_sanitize`, `_validate_url`, `_read_config_url` helpers |
| `anime/constants.py` | Modify | Remove `API_URL`; add the constants listed below |
| `anime/main.py` | Modify | Import `get_api_url` from `.config`; drop `API_URL` import; build `api = AnimeAPI(get_api_url())` as the first line of the final `else:` branch |
| `tests/test_config.py` | Create | pytest suite (names listed in TDD) |
| `pyproject.toml` | Modify | dev extra + pytest config (declarative) |
| `.gitignore` | Modify | add `.pytest_cache/` (declarative) |

### Technical Details

1. **`anime/constants.py`** — delete the line `API_URL = "http://127.0.0.1:8000"` and add exactly:

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
URL_MALFORMED = "malformed URL"
INVALID_CONFIG = "Invalid config file {path}: {reason}"
CONFIG_UNREADABLE = "cannot be read ({error})"
CONFIG_NOT_UTF8 = "not valid UTF-8"
CONFIG_BAD_JSON = "not valid JSON ({error})"
CONFIG_NOT_OBJECT = "top-level value must be a JSON object"
CONFIG_URL_NOT_STRING = '"api_url" must be a string'
```

   The name `API_URL` must not remain anywhere in `anime/` (the new names `DEFAULT_API_URL`, `API_URL_ENV`, `API_URL_KEY` are fine).

2. **`anime/config.py`** — public interface (exact names/signatures; other code and the tests depend on them):

```python
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
    """Validated server URL without trailing '/'.
    Precedence: environ[API_URL_ENV] -> config_file[API_URL_KEY] -> DEFAULT_API_URL.
    Raises ConfigError. Pure: no writes, no prints, no sys.exit.
    The config file is only read when the env var is unset/blank."""


def get_api_url() -> str:
    """resolve_api_url(); on ConfigError print the message to sys.stderr and raise SystemExit(1)."""
```

   Note: `X | None` in annotations is fine on 3.10. Use `config_file_path()` lazily (only when `config_file is None` **and** the env var is blank) — calling `platformdirs` is side-effect free, but keep the order explicit.

3. **Validation algorithm** (`_validate_url(raw, source) -> str | None`, in this order):
   1. `value = raw.strip()`; empty → return `None` (source unset, fall through).
   2. `parts = urllib.parse.urlsplit(value)`; if `urlsplit` raises `ValueError` (e.g. `Invalid IPv6 URL` for an unbalanced `[` such as `http://[::1` or a value containing `\x1b[31m`) → `URL_MALFORMED`. This step is not optional: without it a hostile value produces a traceback.
   3. `parts.scheme.lower() not in {"http", "https"}` → `URL_BAD_SCHEME`. Allow-list on the parsed scheme only — **never** `startswith`/substring checks. (Covers `file://`, `ftp://`, `javascript:`, `nas.local:8000`, missing scheme.)
   4. `parts.username is not None or parts.password is not None` → `URL_CREDENTIALS`.
   5. `not parts.hostname` → `URL_NO_HOST`.
   6. Accessing `parts.port` raises `ValueError` → `URL_BAD_PORT` (`http://host:abc`, and out-of-range ports like `:99999`).
   7. Return `value.rstrip("/")` (path preserved: `http://host/api/` → `http://host/api`).

   On failure raise `ConfigError(INVALID_URL.format(value=_sanitize(shown), source=_sanitize(source), reason=...))` where `shown` is the stripped value, except for `URL_CREDENTIALS` where `shown` is the URL rebuilt without userinfo (the username/password must never appear):

```python
host_part = parts.netloc.rpartition("@")[2]
shown = urlunsplit((parts.scheme, "***@" + host_part, parts.path, parts.query, parts.fragment))
# "http://user:secret@host" -> "http://***@host"
```

   `{source}` = `API_URL_ENV` (`"ANIME_API_URL"`) for the env var, or `str(config_file)` for the file.

4. **Sanitization** (`_sanitize(text: str) -> str`, private): every character for which `str.isprintable()` is False is replaced by its escape; printable characters (including non-ASCII letters like `é`) are kept. Applied to `{value}`, `{source}`, `{path}` and every `{error}` text. Non-obvious detail — this produces `\x1b`, `\n`, `​`:

```python
def _sanitize(text: str) -> str:
    return "".join(
        ch if ch.isprintable() else ch.encode("unicode_escape").decode("ascii")
        for ch in text
    )
```

5. **Config file read** (`_read_config_url(config_file) -> str | None`, returns the raw `api_url` string or `None` when the file/key is absent). Read **only** with `config_file.read_bytes()` — no `open(`, no `.open(` anywhere in the module (an acceptance grep forbids `write_text|write_bytes|mkdir|touch|.open(|open(`, including in docstrings/comments):
   - `FileNotFoundError` → `None` (fall through to default). Catch it **before** the generic `OSError`.
   - other `OSError` as `e` → `CONFIG_UNREADABLE` with `error = e.strerror or type(e).__name__` (directory → `Is a directory`, permission denied → `Permission denied`).
   - `data.decode("utf-8")` raises `UnicodeDecodeError` → `CONFIG_NOT_UTF8`.
   - `json.loads(text)` raises `json.JSONDecodeError` as `e` → `CONFIG_BAD_JSON` with `error = f"line {e.lineno} column {e.colno}"` (never the full message, it can echo file content); `RecursionError` → `CONFIG_BAD_JSON` with `error = "nesting too deep"`. An empty file is invalid JSON (`line 1 column 1`).
   - result not a `dict` → `CONFIG_NOT_OBJECT`.
   - `API_URL_KEY` absent → `None`; present and not `str` (includes `None`/`null`, numbers, objects) → `CONFIG_URL_NOT_STRING`.
   - Every error: `ConfigError(INVALID_CONFIG.format(path=_sanitize(str(config_file)), reason=<reason with sanitized {error}>))`.
   - The returned string then goes through `_validate_url(raw, str(config_file))`.

6. **`resolve_api_url` flow:** `env = os.environ if environ is None else environ` → `_validate_url(env.get(API_URL_ENV, ""), API_URL_ENV)`; non-`None` → return it (config file never read). Otherwise resolve the path, `_read_config_url(...)`; non-`None` raw → `_validate_url(raw, str(path))`; non-`None` → return. Otherwise return `DEFAULT_API_URL`. An invalid set source raises immediately — never fall back.

7. **`get_api_url`:** `try: return resolve_api_url() except ConfigError as e: print(e, file=sys.stderr); raise SystemExit(1)`. Catch **only** `ConfigError` (every expected failure is already converted to it), so no traceback is shown for configuration errors.

8. **`anime/main.py`:** in the import line `from .constants import PARSER_DESCRIPTION,ANINAME_HELP,EP_HELP,RENAME_HELP,EP_ERROR,METADATA,API_URL` drop `API_URL`; add `from .config import get_api_url`. In the final `else:` branch of `main()`, delete `api = AnimeAPI(API_URL)` and make the branch start like this (the rest of the branch is unchanged):

```python
    else:
        api = AnimeAPI(get_api_url())
        anime = watch_input(args.anime_name)
        items = None
        picture = None
        if anime is None:
            return
```

   The `--rename` and `ep<N>` branches are untouched and never call `get_api_url()`. `get_api_url()` appears exactly once as a call in `main.py`. The `Exit` → `main()` recursion re-resolves; that is fine (deterministic, cheap). `anime/api.py` is not modified — it receives the URL already without trailing `/`.

9. **`pyproject.toml`** — add (runtime `dependencies` unchanged; `pytest` must not appear there):

```toml
[project.optional-dependencies]
dev = ["pytest>=7"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

   The `[tool.pytest.ini_options]` section in the repository-root `pyproject.toml` is what anchors pytest's rootdir to this checkout (pytest walks up directories looking for config; this repo is checked out in nested worktrees, so the root `pyproject.toml` must carry it). `pythonpath = ["."]` makes `import anime` resolve to this checkout's package rather than any installed copy. Always run pytest from the repository root. Install for running tests: `pip install -e ".[dev]"` (or `pip install "pytest>=7" platformdirs httpx`).

10. **`.gitignore`** — append `.pytest_cache/`.

**Contract with adjacent layers:**

```
Produces for: anime/main.py (CLI transport)
  - Success: str — validated URL, no trailing "/" (e.g. "http://nas.local:8000")
  - Error: ConfigError(str message) from resolve_api_url — message already sanitized, one line
  - get_api_url(): prints message to stderr + SystemExit(1) on ConfigError

Consumes from: environment (ANIME_API_URL), <user_config_dir("anime")>/config.json (read-only)
  - FileNotFoundError on read_bytes -> absent, fall through to DEFAULT_API_URL
  - any other OSError / decode / JSON / type problem -> ConfigError(INVALID_CONFIG...)

anime/api.py AnimeAPI(url) unchanged: calls f"{url}/anime/search" and f"{url}/anime/{id}".
```
