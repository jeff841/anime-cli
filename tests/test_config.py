import pytest
from platformdirs import user_config_dir
from pathlib import Path

from anime.config import ConfigError, config_file_path, get_api_url, resolve_api_url

DEFAULT = "https://anime-cli.onrender.com"
SCHEME_REASON = "must start with http:// or https://"


@pytest.fixture
def missing(tmp_path):
    return tmp_path / "nope" / "config.json"


@pytest.fixture
def write_cfg(tmp_path):
    def _write(content, name="config.json"):
        path = tmp_path / name
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    return _write


def env_error(value):
    with pytest.raises(ConfigError) as excinfo:
        resolve_api_url({"ANIME_API_URL": value}, Path("/nonexistent-n45-dir/config.json"))
    return str(excinfo.value)


def cfg_error(path):
    with pytest.raises(ConfigError) as excinfo:
        resolve_api_url({}, path)
    return str(excinfo.value)


def test_env_var_wins(missing):
    assert resolve_api_url({"ANIME_API_URL": "http://192.168.1.10:8000"}, missing) == "http://192.168.1.10:8000"


def test_env_var_skips_malformed_config(write_cfg):
    cfg = write_cfg("{bad json")
    assert resolve_api_url({"ANIME_API_URL": "http://192.168.1.10:8000"}, cfg) == "http://192.168.1.10:8000"


def test_config_file_used_when_env_unset(write_cfg):
    cfg = write_cfg('{"api_url": "http://nas.local:8000"}')
    assert resolve_api_url({}, cfg) == "http://nas.local:8000"


def test_default_when_nothing_configured(missing):
    assert resolve_api_url({}, missing) == DEFAULT


def test_config_file_path_location():
    assert config_file_path() == Path(user_config_dir("anime")) / "config.json"


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_env_falls_through(write_cfg, blank):
    cfg = write_cfg('{"api_url": "http://nas.local:8000"}')
    assert resolve_api_url({"ANIME_API_URL": blank}, cfg) == "http://nas.local:8000"


@pytest.mark.parametrize("content", ['{"api_url": ""}', '{"api_url": "  "}'])
def test_blank_api_url_falls_back_to_default(write_cfg, content):
    assert resolve_api_url({}, write_cfg(content)) == DEFAULT


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("http://nas.local:8000/", "http://nas.local:8000"),
        ("http://host/api//", "http://host/api"),
        ("  http://host:9000  ", "http://host:9000"),
    ],
)
def test_url_normalization(missing, raw, expected):
    assert resolve_api_url({"ANIME_API_URL": raw}, missing) == expected


@pytest.mark.parametrize(
    "value", ["nas.local:8000", "file:///etc/passwd", "ftp://host", "javascript:alert(1)"]
)
def test_bad_scheme_rejected(value):
    assert env_error(value) == f'Invalid server URL "{value}" (from ANIME_API_URL): {SCHEME_REASON}'


def test_uppercase_https_accepted(missing):
    assert resolve_api_url({"ANIME_API_URL": "HTTPS://Host:8443"}, missing) == "HTTPS://Host:8443"


@pytest.mark.parametrize("value", ["http://", "http:///path"])
def test_missing_host_rejected(value):
    assert env_error(value) == f'Invalid server URL "{value}" (from ANIME_API_URL): missing host'


@pytest.mark.parametrize("value", ["http://host:abc", "http://host:99999"])
def test_invalid_port_rejected(value):
    assert env_error(value) == f'Invalid server URL "{value}" (from ANIME_API_URL): invalid port'


def test_malformed_url_rejected():
    assert env_error("http://[::1") == 'Invalid server URL "http://[::1" (from ANIME_API_URL): malformed URL'


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


def test_get_api_url_returns_resolved_url(monkeypatch):
    monkeypatch.setenv("ANIME_API_URL", "http://nas.local:8000/")
    assert get_api_url() == "http://nas.local:8000"


def test_config_bad_json(write_cfg):
    cfg = write_cfg("{bad json")
    assert cfg_error(cfg) == f"Invalid config file {cfg}: not valid JSON (line 1 column 2)"


def test_config_empty_file(write_cfg):
    cfg = write_cfg("")
    assert cfg_error(cfg) == f"Invalid config file {cfg}: not valid JSON (line 1 column 1)"


def test_config_not_utf8(write_cfg):
    cfg = write_cfg(b"\xff\xfe")
    assert cfg_error(cfg) == f"Invalid config file {cfg}: not valid UTF-8"


def test_config_not_object(write_cfg):
    cfg = write_cfg("[]")
    assert cfg_error(cfg) == f"Invalid config file {cfg}: top-level value must be a JSON object"


@pytest.mark.parametrize("content", ['{"api_url": 8000}', '{"api_url": null}'])
def test_config_api_url_not_string(write_cfg, content):
    cfg = write_cfg(content)
    assert cfg_error(cfg) == f'Invalid config file {cfg}: "api_url" must be a string'


def test_config_path_is_directory(tmp_path):
    msg = cfg_error(tmp_path)
    assert msg.startswith(f"Invalid config file {tmp_path}: cannot be read (")
    assert msg.endswith(")")


def test_config_deeply_nested_json(write_cfg):
    cfg = write_cfg("[" * 100000)
    assert cfg_error(cfg) == f"Invalid config file {cfg}: not valid JSON (nesting too deep)"


def test_config_key_absent_returns_default(write_cfg):
    assert resolve_api_url({}, write_cfg('{"other": 1}')) == DEFAULT


def test_config_invalid_url_names_file(write_cfg):
    cfg = write_cfg('{"api_url": "ftp://x"}')
    assert cfg_error(cfg) == f'Invalid server URL "ftp://x" (from {cfg}): {SCHEME_REASON}'


def test_credentials_rejected_and_redacted():
    msg = env_error("http://user:secret@host")
    assert msg == 'Invalid server URL "http://***@host" (from ANIME_API_URL): must not contain credentials'
    assert "user" not in msg and "secret" not in msg


def test_control_chars_escaped():
    msg = env_error("ftp://ho\nst\x1b[31m")
    assert msg == 'Invalid server URL "ftp://ho\\nst\\x1b[31m" (from ANIME_API_URL): malformed URL'
    assert "\\x1b" in msg and "\\n" in msg
    assert "\x1b" not in msg and "\n" not in msg


def test_non_ascii_kept():
    assert 'Invalid server URL "ftp://café"' in env_error("ftp://café")


def test_resolver_creates_nothing(tmp_path):
    newdir = tmp_path / "newdir"
    assert resolve_api_url({}, newdir / "config.json") == DEFAULT
    assert not newdir.exists()
