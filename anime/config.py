import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from platformdirs import user_config_dir

from .constants import (
    API_URL_ENV,
    API_URL_KEY,
    CONFIG,
    CONFIG_BAD_JSON,
    CONFIG_JSON,
    CONFIG_NOT_OBJECT,
    CONFIG_NOT_UTF8,
    CONFIG_UNREADABLE,
    CONFIG_URL_NOT_STRING,
    DEFAULT_API_URL,
    INVALID_CONFIG,
    INVALID_URL,
    URL_BAD_PORT,
    URL_BAD_SCHEME,
    URL_CREDENTIALS,
    URL_MALFORMED,
    URL_NO_HOST,
)


class ConfigError(Exception):
    """Raised with an already-formatted, safe, one-line user message."""


def config_file_path() -> Path:
    """Return Path(user_config_dir(CONFIG)) / CONFIG_JSON. Never creates anything."""
    return Path(user_config_dir(CONFIG)) / CONFIG_JSON


def _sanitize(text: str) -> str:
    return "".join(
        ch if ch.isprintable() else ch.encode("unicode_escape").decode("ascii")
        for ch in text
    )


def _invalid_url(shown: str, source: str, reason: str) -> ConfigError:
    return ConfigError(
        INVALID_URL.format(value=_sanitize(shown), source=_sanitize(source), reason=reason)
    )


def _validate_url(raw: str, source: str) -> str | None:
    value = raw.strip()
    if not value:
        return None
    try:
        parts = urlsplit(value)
    except ValueError:
        raise _invalid_url(value, source, URL_MALFORMED) from None
    if parts.scheme.lower() not in {"http", "https"}:
        raise _invalid_url(value, source, URL_BAD_SCHEME)
    if parts.username is not None or parts.password is not None:
        host_part = parts.netloc.rpartition("@")[2]
        shown = urlunsplit(
            (parts.scheme, "***@" + host_part, parts.path, parts.query, parts.fragment)
        )
        raise _invalid_url(shown, source, URL_CREDENTIALS)
    if not parts.hostname:
        raise _invalid_url(value, source, URL_NO_HOST)
    try:
        parts.port
    except ValueError:
        raise _invalid_url(value, source, URL_BAD_PORT) from None
    return value.rstrip("/")


def _read_config_url(config_file: Path) -> str | None:
    def invalid(reason: str) -> ConfigError:
        return ConfigError(
            INVALID_CONFIG.format(path=_sanitize(str(config_file)), reason=reason)
        )

    try:
        data = config_file.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as e:
        error = _sanitize(e.strerror or type(e).__name__)
        raise invalid(CONFIG_UNREADABLE.format(error=error)) from None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise invalid(CONFIG_NOT_UTF8) from None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        error = f"line {e.lineno} column {e.colno}"
        raise invalid(CONFIG_BAD_JSON.format(error=error)) from None
    except RecursionError:
        raise invalid(CONFIG_BAD_JSON.format(error="nesting too deep")) from None
    if not isinstance(parsed, dict):
        raise invalid(CONFIG_NOT_OBJECT)
    if API_URL_KEY not in parsed:
        return None
    url = parsed[API_URL_KEY]
    if not isinstance(url, str):
        raise invalid(CONFIG_URL_NOT_STRING)
    return url


def resolve_api_url(
    environ: Mapping[str, str] | None = None,
    config_file: Path | None = None,
) -> str:
    """Validated server URL without trailing '/'.
    Precedence: environ[API_URL_ENV] -> config_file[API_URL_KEY] -> DEFAULT_API_URL.
    Raises ConfigError. Pure: no writes, no prints, no sys.exit.
    The config file is only read when the env var is unset/blank."""
    env = os.environ if environ is None else environ
    url = _validate_url(env.get(API_URL_ENV, ""), API_URL_ENV)
    if url is not None:
        return url
    path = config_file_path() if config_file is None else config_file
    raw = _read_config_url(path)
    if raw is not None:
        url = _validate_url(raw, str(path))
        if url is not None:
            return url
    return DEFAULT_API_URL


def get_api_url() -> str:
    """resolve_api_url(); on ConfigError print the message to sys.stderr and raise SystemExit(1)."""
    try:
        return resolve_api_url()
    except ConfigError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
