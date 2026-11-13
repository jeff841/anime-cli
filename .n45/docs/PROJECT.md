---
created_at: "2026-11-13 10:41:11"
description: Terminal-based anime manager and player with MyAnimeList metadata
n45_version: 1.1.0
type: CLI
updated_at: "2026-11-13 11:20:23"
---
## Overview

A terminal-based anime manager and player. It lists series folders from a user-chosen directory, plays episodes through VLC, tracks watched episodes by renaming files, renames episode files to the expected scheme, and shows MyAnimeList metadata (synopsis, genres, cover) fetched through a local proxy server.

**Type:** CLI
**Access model:** public / single user, local
**Multi-tenant:** no, single-tenant

## Personas and Profiles

| Persona | Who | JTBD |
| ------- | --- | ---- |
| Local anime watcher | Person with a local anime collection | Browse, play in order, and resume watching from the terminal |

**Profiles:** a single local user with filesystem access; no authentication or roles.

## Modules / Domains

| Module | Responsibility |
| ------ | -------------- |
| Collection browsing | Configure the collection directory, list series and episodes (`watch_input`, `show`) |
| Playback | Launch VLC for episodes and mark them watched (`play`, `extra`, `reset_watched`) |
| Renaming | Normalize filenames to `ep<N>-` (`renamer`) |
| Metadata | Fetch and display MAL info and cover (`api`, `picture`, `kitty`, `cli`) |
| Metadata server | Proxy and cache MAL API (`server/`) |

## Main Flows

### Watch a series

1. User runs `anime` or `anime <name> [ep<N>]`
2. On first run the user picks the directory containing series folders (saved to config)
3. User selects a series and an episode
4. System plays the episode in VLC fullscreen, renames the file with the `watched` suffix, then continues with the next episode
5. Deviation: VLC missing -> RuntimeError

### Attach MyAnimeList info

1. User chooses "Get anime information" in the series menu
2. Enters a name; system searches via the server and lists results
3. User picks one; system stores `{"id": ...}` in `anime.json` and shows title, synopsis, genres and cover (kitty only)
4. Deviation: server unreachable -> unhandled HTTP error

## Business Rules

- Episodes are identified by filename prefix `ep`, `op`, `ed`; ordering uses the number between the prefix and the first `-`
- An episode is watched when its filename ends with `watched`
- Series metadata lives in `anime.json` inside the series folder and is excluded from episode listings
- The collection directory must contain only series folders
- `--rename` renames every file in the target directory to `ep<N>-` in sorted order, destroying the original names
- The metadata server URL comes from `ANIME_API_URL`, then `api_url` in `config.json`, then `http://127.0.0.1:8000`; an invalid configured value aborts startup of the interactive menu with exit code 1 and one error line

## Limits

- Search returns at most 10 results; search cache TTL 1 day, details cache TTL 7 days
- Menu requires terminal width of at least 90 columns

## External Integrations

| Service | Purpose | Protocol |
| ------- | ------- | -------- |
| MyAnimeList API v2 | Metadata and cover images | REST |
| VLC | Playback | Subprocess |
| kitty icat | Cover image rendering | Subprocess |

## Glossary

| Term | Definition |
| ---- | ---------- |
| watched | Filename suffix marking a played episode |
| Extras | Subfolder of a series holding op/ed/extra episodes |
| MAL | MyAnimeList |
