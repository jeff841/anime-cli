# anime-cli

A terminal-based anime manager and player for organizing, browsing, and watching local anime collections.

`anime-cli` provides a `curses` interface for selecting series and episodes, launches episodes with VLC, tracks watched status, renames episode files into the format expected by the application, and retrieves anime information from MyAnimeList through a hosted API.

## Features

- Browse an anime collection from the terminal.
- Select anime and episodes with the keyboard or mouse.
- Play episodes with VLC.
- Track watched episodes and reset watched status.
- Automatically select the first unwatched episode when requested.
- Rename episode files into the application's `ep<number>-` format.
- Add series directories to the configured collection.
- Move series out of the collection.
- Search MyAnimeList and display anime metadata and artwork.
- Keep configuration in the user's configuration directory instead of the project directory.
- Use a hosted API so the MAL client ID never has to be installed on the user's machine.

## Requirements

- Python 3.10 or newer
- VLC
- `pipx` (recommended for installation)
- A terminal with `curses` support
- Internet access for MyAnimeList features

VLC must be installed and available on your `PATH`.

On Arch Linux:

```bash
sudo pacman -S vlc python-pipx
pipx ensurepath
```

Restart your shell after `pipx ensurepath` if necessary.

On Windows, install Python, VLC, and `pipx`. The package installs `windows-curses` automatically on Windows.

## Installation

### From PyPI

When the package is published to PyPI:

```bash
pipx install anime-ctl
```

The installed command is:

```bash
anime
```

The package name is `anime-ctl`, while the executable remains `anime`.

### From a local checkout

Clone the repository and install it in an isolated environment with `pipx`:

```bash
git clone https://github.com/jeff841/anime-cli.git
cd anime-cli
pipx install .
```

For a development installation, use a virtual environment instead:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

On Windows, activate the environment with the corresponding Windows activation command.

## Usage

### Start the application

```bash
anime
```

The first launch asks you to select the directory containing your series folders. The directory is saved in the user's application configuration and is reused on subsequent launches.

You can also open a specific anime directly:

```bash
anime "Nisekoi"
```

### Play an episode directly

```bash
anime "Nisekoi" ep1
```

Episode names use the form `ep<number>`, for example `ep1`, `ep2`, or `ep10`.

### Command-line actions

Add a series to the configured collection:

```bash
anime --add /path/to/Nisekoi
```

The directory is moved into the collection rather than copied. An existing series with the same name is not overwritten.

Move a series out of the collection:

```bash
anime --move "Nisekoi" /path/to/destination
```

If no destination is specified, the series is moved to your home directory:

```bash
anime --move "Nisekoi"
```

Rename the files in a series directory:

```bash
anime --rename /path/to/Nisekoi
```

Running `--rename` without a path opens an interactive directory-selection menu:

```bash
anime --rename
```

### Interactive commands

Press `:` inside a menu to open the command line.

The available commands include:

| Command | Description |
| --- | --- |
| `open <entry>` / `o` | Open an entry by menu number or exact name. |
| `play <anime> [episode]` / `p` | Play an anime, optionally starting at a specified episode. |
| `play [episode]` / `p` | From an episode menu, play the current anime. |
| `rename <anime>` | Rename another series in the collection. |
| `rename [anime]` | Rename the current series or a named series. |
| `add <directory>` | Add a series directory to the collection. |
| `move <anime> [destination]` | Move a series out of the collection. |
| `quit` / `q` | Exit the application or return to the previous menu. |

The main menu also provides actions for adding a series, changing the anime directory, and exiting. The episode menu provides actions for renaming, retrieving anime information, resetting watched status, and returning to the collection.

## Anime Directory Structure

The configured directory should contain one directory per series:

```text
~/anime/
├── Nisekoi/
│   ├── ep1-
│   ├── ep2-
│   └── ep3-
├── Naruto/
│   ├── ep1-
│   ├── ep2-
│   └── ep3-
└── One Piece/
    ├── ep1-
    ├── ep2-
    └── ep3-
```

`anime-cli` treats the directories immediately inside the configured directory as anime series.

## Renaming Episodes

The renamer sorts the files in a series directory and renames them sequentially:

```text
original-file-1.mkv  ->  ep1-
original-file-2.mkv  ->  ep2-
original-file-3.mkv  ->  ep3-
```

The generated names are the format currently expected by the application. `anime.json` is excluded from the rename operation.

**Back up important files before using the renamer.** Renaming changes the files in place and is not reversible by `anime-cli`.

## Configuration

Configuration is stored using the platform's standard user configuration directory through `platformdirs`.

The anime collection path is stored in a file named `directory.json` under the application's configuration directory. Its contents have the following form:

```json
{
    "anime_list": "/path/to/your/anime"
}
```

The application creates the configuration directory and file when needed.

To change the configured collection directory, use the **Change anime directory** option in the main menu.

Personal configuration should not be committed to Git.

## MyAnimeList Integration

MyAnimeList requests are made through the project's hosted API rather than directly from the installed CLI.

```text
┌────────────┐       HTTPS       ┌──────────────────┐       HTTPS       ┌──────────────┐
│ anime-cli  │ ─────────────────> │ anime-cli API    │ ───────────────> │ MyAnimeList  │
│            │                    │                  │                  │ API          │
└────────────┘                    └──────────────────┘                  └──────────────┘
                                         │
                                         │ MAL_CLIENT_ID
                                         ▼
                                  Server environment
```

The MAL client ID is stored only on the API server as the `MAL_CLIENT_ID` environment variable. It is not part of the CLI package and users do not need to create a MyAnimeList developer application or configure a MAL credential locally.

The CLI currently uses these API endpoints:

```text
GET /
GET /anime/search?q=<name>
GET /anime/<id>
```

The API caches search results for 24 hours and anime details for 7 days using SQLite.

The production API URL is currently configured as:

```text
https://anime-cli.onrender.com
```

### Local API development

The API server can be run locally from the repository root.

Set the MAL client ID in your environment:

```bash
export MAL_CLIENT_ID="your_client_id"
```

Then start the server:

```bash
uvicorn server.main:app --reload
```

The CLI's production API URL is defined in `anime/constants.py`. For local development, point the CLI at your local API by changing that value or using the API URL override supported by your local source version.

**Never commit a real MAL client ID to Git.**

### Render deployment

The repository includes `render.yaml` and `server/Dockerfile` for deploying the API to Render. The deployment uses the `MAL_CLIENT_ID` environment variable as a secret and exposes the server on the port supplied by Render.

## Metadata and Artwork

When anime information is selected from the MyAnimeList search, the series directory receives an `anime.json` file containing the selected MyAnimeList anime ID.

The application uses that ID to retrieve metadata such as:

- Title
- Synopsis
- Number of episodes
- Rating
- Genres
- Main artwork

Artwork is displayed in terminals where Kitty graphics are available. The interface also works without Kitty; artwork is simply not displayed.

## Building

Install the build frontend:

```bash
python -m pip install build
```

Build the package:

```bash
python -m build
```

The generated distribution files are placed in `dist/`.

To test a wheel with `pipx`:

```bash
pipx install ./dist/<wheel-file>.whl
```

If the package is already installed, reinstall the wheel:

```bash
pipx reinstall ./dist/<wheel-file>.whl
```

Test the installed command outside the repository:

```bash
cd ~
anime --help
```

This helps verify that the application is using the installed package rather than the source checkout.

## Development

Clone the repository:

```bash
git clone https://github.com/jeff841/anime-cli.git
cd anime-cli
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

The project uses `setuptools` for packaging. The Python package is `anime`, while the distribution/project name is `anime-ctl` and the command-line entry point is `anime`.

## Project Structure

```text
anime-cli/
├── anime/
│   ├── __init__.py
│   ├── __main__.py
│   ├── anime_details.py
│   ├── cli.py
│   ├── collection.py
│   ├── commands.py
│   ├── constants.py
│   ├── episode.py
│   ├── extra.py
│   ├── kitty.py
│   ├── main.py
│   ├── menu_result.py
│   ├── picture.py
│   ├── play.py
│   ├── remote_api.py
│   ├── renamer.py
│   ├── reset_watched.py
│   ├── show.py
│   └── watch_input.py
├── server/
│   ├── __init__.py
│   ├── cache.py
│   ├── config.py
│   ├── main.py
│   ├── mal.py
│   ├── Dockerfile
│   └── requirements.txt
├── render.yaml
├── pyproject.toml
├── README.md
└── .gitignore
```

## Git and Generated Files

Do not commit local environments, build artifacts, caches, or personal configuration. A suitable `.gitignore` includes entries such as:

```gitignore
.venv/
__pycache__/
*.py[cod]
build/
dist/
*.egg-info/
*.db
.env
```

The source code, `pyproject.toml`, README, deployment configuration, and other project files required to build or deploy the application should be committed.

## License

The project metadata currently declares the MIT license. Add a `LICENSE` file to the repository if the project is intended to be distributed publicly under MIT.

## Status

`anime-cli` is an early-stage project. The command-line interface, packaging, hosted API, and feature set are still evolving.
