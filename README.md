# anime-cli

A terminal-based anime manager and player for organizing and watching anime episodes.

`anime-cli` can organize episode files into the structure expected by the application, search MyAnimeList for anime information, and launch episodes through VLC.

## Features

* Browse your anime collection from the terminal.
* Play episodes using VLC.
* Keep track of watched episodes.
* Organize episode filenames.
* Rename an existing series directory with `--rename`.
* Search MyAnimeList for anime information.
* Store application configuration outside the project directory.
* Terminal interface using `curses`.

## Requirements

* Python 3.10 or newer
* VLC
* `pipx`
* A MyAnimeList API connection for MAL-related features

VLC must be available as an executable on your system.

### Linux

On Arch Linux:

```bash
sudo pacman -S vlc python-pipx
```

Then make sure `pipx` applications are available on your `PATH`:

```bash
pipx ensurepath
```

Restart your shell after running `pipx ensurepath`.

### Windows

Install Python, VLC, and `pipx`. Make sure both Python and VLC are available to the application.

## Installation

`anime-cli` is installed with `pipx`, which keeps the application's Python dependencies isolated while making the `anime` command available globally.

### From PyPI

Once the package is published:

```bash
pipx install anime-cli
```

After installation, run:

```bash
anime
```

The command works regardless of your current directory.

### From a local wheel

To install a locally built version:

```bash
pipx install ./dist/anime_cli-0.1.0-py3-none-any.whl
```

You can then use:

```bash
anime
```

from any directory.

## Usage

### Open the anime menu

```bash
anime
```

This opens the main menu where you can browse your configured anime directory.

### Menu commands

Press `:` in a menu to open its internal command line. The following commands
are currently available:

* `open <entry>` (or `o`) — open an entry by its one-based menu number or exact name;
  for example, `open 2` or `open Nisekoi`.
* `play <anime> [episode]` (or `p`) — from the anime-selection menu, play an
  anime from its first unwatched episode, or from an optional episode such as
  `ep3`. For example: `play Nisekoi ep3`.
* `play [episode]` (or `p`) — from an episode-selection menu, play the current
  anime from its first unwatched episode, or from the specified episode.
* `quit` (or `q`) — exit `anime-cli`.

### Open an anime directly

```bash
anime "anime name"
```

For example:

```bash
anime nisekoi
```

### Play an episode

An episode can be selected through the anime menu or specified after the anime name:

```bash
anime nisekoi ep1
```

## Directory Structure

`anime-cli` expects your anime collection to be organized approximately like this:

```text
anime/
├── Nisekoi/
│   ├── ep1-...
│   ├── ep2-...
│   └── ep3-...
│
├── Naruto/
│   ├── ep1-...
│   ├── ep2-...
│   └── ep3-...
│
└── One Piece/
    ├── ep1-...
    ├── ep2-...
    └── ep3-...
```

The configured directory should contain the **series folders**, rather than being a single series folder.

## Renaming Episodes

If your episodes aren't using the naming structure expected by `anime-cli`, use:

```bash
anime --rename
```

This opens a menu allowing you to:

1. Enter a directory path.
2. Select a directory using a file explorer.
3. Exit.

You can also provide the directory directly:

```bash
anime --rename /path/to/anime
```

For example:

```bash
anime --rename ~/Downloads/Nisekoi
```

The renamer converts the files into the episode naming scheme used by the application.

> Make sure you have a backup if the directory contains files you don't want renamed.

## Configuration

Application configuration is stored in the user's configuration directory rather than inside the project.

The application creates its configuration directory automatically when needed.

The configured anime directory is stored in a structure similar to:

```json
{
    "anime_list": "/path/to/your/anime"
}
```

Personal configuration files should not be committed to the project repository.

## MyAnimeList

`anime-cli` uses the MyAnimeList API for anime information.

API configuration is handled by the application. Users should not need to commit or distribute API credentials.

If local credentials are required by a development installation, store them in a local `.env` file:

```env
MAL_CLIENT_ID=your_client_id
```

Never commit `.env` or other credentials to Git.

## Cache

`anime-cli` may maintain a local cache database.

The cache contains runtime data and should not be committed to the repository.

For example, a Git repository should ignore:

```gitignore
*.db
```

## Updating

If `anime-cli` was installed with `pipx`, update it with:

```bash
pipx upgrade anime-cli
```

If a new release is available on PyPI, `pipx` will install the updated version.

## Uninstalling

To remove `anime-cli`:

```bash
pipx uninstall anime-cli
```

## Development

Clone the repository:

```bash
git clone https://github.com/jeff841/anime-cli
cd anime-cli
```

Create a development virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

This allows changes to the source code to be tested without rebuilding the package after every change.

## Building

Install the Python build frontend:

```bash
python -m pip install build
```

Build the package:

```bash
python -m build
```

This creates the distribution files in `dist/`:

```text
dist/
├── anime_cli-0.1.0-py3-none-any.whl
└── anime_cli-0.1.0.tar.gz
```

### Test the built wheel with pipx

You can test the exact wheel that will be distributed:

```bash
pipx install ./dist/anime_cli-0.1.0-py3-none-any.whl
```

Then test the application from outside the repository:

```bash
cd ~
anime --help
```

This verifies that the installed package works independently of the source directory.

If the package is already installed, reinstall the newly built wheel:

```bash
pipx reinstall ./dist/anime_cli-0.1.0-py3-none-any.whl
```

## Git

Generated files and local configuration should not be committed.

A suitable `.gitignore` includes:

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

Source code, `pyproject.toml`, documentation, and other files required to build and distribute the application should be committed.

## Project Structure

```text
anime-cli/
├── anime/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api.py
│   ├── cli.py
│   ├── episode.py
│   ├── extra.py
│   ├── kitty.py
│   ├── main.py
│   ├── picture.py
│   ├── play.py
│   ├── renamer.py
│   ├── reset_watched.py
│   ├── show.py
│   └── watch_input.py
├── README.md
├── pyproject.toml
└── .gitignore
```

## License

Add your chosen license here before publishing the project.

## Status

`anime-cli` is currently in early development.

The `0.1.0` release is an initial release while the application's interface and features continue to mature.
