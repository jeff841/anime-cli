---
created_at: "2026-11-13 10:50:21"
from: security
n45_version: 1.1.0
spec_id: feat-0001-configurable-server-url
---
### Abuse Scenarios (red team)

Context: a local CLI whose server URL is now user-configurable via env var or config file. The server returns JSON that the CLI renders in curses and uses to download a cover image. The attacker is mainly (a) someone who can influence the env or config file, or (b) a malicious or compromised server the CLI is pointed at, or a network MITM on plain http.

| Vector | Attack (what the attacker does) | Required mitigation | Severity |
| --- | --- | --- | --- |
| `ANIME_API_URL` / `config.json` `api_url` | Points the CLI at an attacker-controlled host (poisoned shell profile, shared config, malicious dotfile) to feed forged metadata | Accept only `http`/`https` with a non-empty host; fail-closed (exit 1) on any invalid value; never fall back silently to another source after a source was set but invalid | Medium |
| URL scheme | Value like `file://`, `ftp://`, `gopher://` or `javascript:` to reach local files or unintended protocols through the HTTP client | Strict scheme allow-list (`http`, `https`) via parsed URL, not substring or prefix matching | Medium |
| URL userinfo | `http://user:pass@host` leaks credentials in the process list, logs or error messages, and may be echoed back by the invalid-URL message | Reject URLs containing userinfo (username/password), or at minimum never print them in error messages | Medium |
| Error messages | The invalid-URL message echoes the raw value, which could contain embedded secrets or terminal escape sequences from env or config | Escape or repr-quote the value when printing (neutralize control and ANSI escape characters); apply the same to the config path and JSON error reason | Low |
| Plain http to a remote host | MITM on LAN/NAS traffic tampers with metadata (title, synopsis, `main_picture.large` URL) | Document that `https` is recommended for non-loopback hosts; do not block `http` (LAN use case is the feature). Optionally a one-time warning for `http` to a non-loopback host | Low |
| Server-supplied image URL (`main_picture.large`) | A malicious configured server returns an arbitrary URL (internal address, huge file) that the CLI downloads via `requests` | Out of scope of the resolver, but the spec must state that the configured server is trusted: not a new boundary created by the resolver. Recommend a follow-up for timeout and size cap on the image download | Medium |
| Server-supplied text in curses | Malicious server returns terminal escape sequences in title/synopsis | Pre-existing; note as follow-up (strip control characters before rendering). Not part of this feature | Low |
| `config.json` parsing | Oversized or deeply nested JSON, or wrong types, crash the CLI with a stack trace | Catch `JSONDecodeError`, `OSError`, `UnicodeDecodeError` and non-object top level; clear one-line error, exit 1, no traceback | Low |
| Config file permissions / location | Another local user pre-creates or replaces the config file | File lives in the per-user config dir (platformdirs); the resolver must not create the file, must not follow a path outside that dir, and holds no secrets. Nothing more required | Low |
| Env var precedence | Env var silently overrides a file the user trusts | Documented precedence (env > file > default); no redirect following or discovery beyond these three sources | Low |

### Implementation Requirements — Critical / High

None. No Critical or High vector exists: the feature adds no network listener, no authentication, no persistence of secrets, and the server (`server/`) is untouched.

### Implementation Requirements — Medium / Low

- The URL is parsed with the standard parser; scheme must be exactly `http` or `https` (case-insensitive) and the host non-empty; any other value is fail-closed (exit 1, message to stderr).
- URLs containing userinfo are rejected, and no error message ever prints credentials.
- Values echoed in error messages (URL, config path, JSON reason) are rendered with control and escape characters neutralized.
- Reading `config.json` handles `JSONDecodeError`, `OSError`, `UnicodeDecodeError` and non-object top-level JSON with a single clear error and exit 1; no traceback is ever shown.
- The resolver never creates, writes or modifies the config file, and never reads any other source than env var, `config.json` and the default.
- Resolution is lazy (only where `AnimeAPI` is built), so `--rename` and direct playback are not blocked by a bad URL (as already specified).
- README states that the configured server is trusted and recommends `https` for non-loopback hosts.
- Tests cover: `file://`, `ftp://`, missing scheme, empty host, userinfo, control characters in the value (error message safe).
- Follow-ups (outside this spec, record as notes): timeout and size cap on the cover image download, and stripping control characters from server-supplied text before curses rendering.

### For tasks

- `50a8844c7d`: Strict allow-list validation (scheme, host, no userinfo) fail-closed; resolver with no side effects on the filesystem; safe error messages (escaped values, no traceback); tests for the hostile inputs above.
- `844dd534f4`: Not applicable (no web frontend).
- `82654b3833`: Not applicable to server or infra; only `pytest` as a dev-only extra (not a runtime dependency), pinned lower-bound, no secrets involved.
