---
entries:
    - date: "2026-11-13"
      feature: feat-0001-configurable-server-url
      summary: |
        ### Adicionado
        - Configurable metadata server URL: `ANIME_API_URL` environment variable, `api_url` key in `config.json` (platformdirs config dir), default `http://127.0.0.1:8000`; value is trimmed, trailing slashes removed, and validated (http/https, host, port, no credentials) (TASK-001)
        - pytest suite for URL resolution (`tests/test_config.py`) and `dev` extra in `pyproject.toml` (TASK-001)
        - README documentation for server URL configuration and running tests (TASK-002)
        ### Alterado
        - `API_URL` constant replaced by `DEFAULT_API_URL`; the URL is resolved in `anime/config.py` when the interactive menu starts. An invalid URL or malformed `config.json` prints one error line and exits with code 1 (TASK-001)
      version: 0.1.0
n45_version: 1.1.0
---
