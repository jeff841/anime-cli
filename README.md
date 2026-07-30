
# Anime Player

A simple terminal-based anime player written in Python. It provides a curses-based interface for selecting a series and episode, launches VLC in fullscreen, and automatically keeps track of watched episodes.

## Features

* Browse your anime library from a terminal menu.
* Choose the directory where your anime collection is stored.
* Remembers the selected anime directory between launches.
* Change the root anime directory at any time through the CLI.
* Browse episodes in numerical order.
* Plays episodes using **VLC** in fullscreen.
* Automatically marks watched episodes.
* Reset watched status for a series or extras.
* Built-in episode renamer.
* Installable as a terminal command.

## Requirements

* Python 3.10+
* VLC installed and available in your `PATH`
* Linux or another Unix-like operating system

## Installation

### Using pipx (recommended)

Install pipx:

### Arch Linux

```bash
sudo pacman -S python-pipx
```

Enable pipx:

```bash
pipx ensurepath
```

Restart your terminal, then clone the repository:

```bash
git clone https://github.com/<your-username>/anime-cli.git
cd anime-cli
```

Install:

```bash
pipx install .
```

The player is now available as:

```bash
anime
```

### Development installation

If you want to modify the project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Then run:

```bash
anime
```

## Usage

Start the player:

```bash
anime
```

On the first launch, you will be asked for the directory containing your anime series.

Example:

```
Anime/
├── Frieren/
├── Bocchi the Rock/
├── Vinland Saga/
└── Steins;Gate/
```

The selected directory is saved automatically. If you move your anime collection, select:

```
Change anime directory
```

from the menu.

## Renaming Episodes

The player includes a renaming utility to standardize episode filenames.

Run:

```bash
anime rename /path/to/series
```

Episodes are renamed into the format:

```
ep1-
ep2-
ep3-
...
```

The player uses this naming scheme to sort episodes correctly.

## Episode Ordering

Episodes are sorted numerically.

Example:

```
ep1-
ep2-
ep3-
ep10-
ep11-
```

instead of alphabetical sorting:

```
ep1-
ep10-
ep11-
ep2-
```

Openings (`op`), endings (`ed`), and episodes (`ep`) are supported.

## Watched Episodes

After an episode finishes playing, it is marked as watched by appending:

```
watched
```

Example:

Before:

```
ep5-
```

After:

```
ep5-watched
```

You can restore filenames using:

```
Reset watched status
```

from the menu.

## Extras

Series can contain an `Extras` directory for additional content.

Example:

```
Frieren/
├── ep1-
├── ep2-
├── ep3-
└── Extras/
    ├── op1-
    └── ed1-
```

Extras support:

* VLC playback
* episode sorting
* watched tracking
* resetting watched status

## Project Structure

```
anime-cli/
├── anime/
│   ├── main.py
│   ├── cli.py
│   └── renamer.py
├── pyproject.toml
├── README.md
└── directory.json
```

## License

This project is released under the MIT License.

