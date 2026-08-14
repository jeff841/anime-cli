# anime-cli

A terminal-based anime manager and player for organizing and watching anime episodes.

`anime-cli` can organize episode files into the structure expected by the application, search MyAnimeList for anime information, and launch episodes through VLC.

## Features

* Browse your anime collection from the terminal.
* Play episodes using VLC.
* Keep track of watched episodes.
* Automatically organize episode filenames.
* Rename an existing series directory with `--rename`.
* Search MyAnimeList for anime information.
* Store application configuration outside the project directory.
* Terminal interface using `curses`.

## Requirements

* Python 3.10 or newer
* VLC

VLC must be available as an executable on your system.

### Linux

Install VLC using your distribution's package manager. On Arch Linux:

```bash
sudo pacman -S vlc
```

### Windows

Install VLC and make sure its executable is available to the application.

## Installation

Install the package from a built wheel:

```bash
pip install anime_cli-0.1.0-py3-none-any.whl
```

Or install the project locally:

```bash
pip install .
```

After installation, the `anime` command is available:

```bash
anime
```

## Usage

### Open the anime menu

```bash
anime
```

This opens the main menu where you can browse your configured anime directory.

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

The exact episode selection depends on the episode files in the series directory.

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

The directory selected in the application should contain the **series folders**, rather than being a single series folder.

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

Configuration includes information such as the location of your anime collection.

The configuration is conceptually structured like:

```json
{
    "anime_list": "/path/to/your/anime"
}
```

Do not manually commit your personal configuration files to the repository.

## MyAnimeList API

Some functionality uses the MyAnimeList API.

## Cache

The application may maintain a local cache database.

The cache is runtime data and should not be committed to the repository.

For example:

```gitignore
*.db
```

A user's cache can be recreated when necessary.

## Development

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/jeff841/anime-cli
cd anime-cli

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

Test the wheel in a clean environment before publishing:

```bash
python -m venv /tmp/anime-test
source /tmp/anime-test/bin/activate
pip install dist/*.whl
anime --help
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

## Status

`anime-cli` is currently in early development.

The `0.1.0` release should be considered an initial release while the application interface and features continue to mature.

