
# Anime Player

A terminal-based anime player written in Python. It provides a curses interface for browsing your anime library, launches episodes in VLC, automatically tracks watched episodes, and includes a built-in episode renamer.

## Features

* Browse your anime library through a terminal interface.
* Select your anime library by:

  * typing its path manually, or
  * choosing it with a graphical folder picker.
* Remembers your selected library between launches.
* Change the anime library at any time from the main menu.
* Browse episodes in numerical order.
* Supports regular episodes (`ep`), openings (`op`), endings (`ed`), and an optional `Extras` directory.
* Plays episodes in **VLC** in fullscreen.
* Automatically continues to the next episode after playback.
* Automatically marks watched episodes.
* Reset watched status for an entire series or its `Extras` folder.
* Built-in episode renamer.
* Installable as the `anime` terminal command.

## Requirements

* Python 3.10 or newer
* VLC installed and available in your `PATH`
* Linux (tested on Arch Linux)

## Installation

### Install pipx (recommended)

#### Arch Linux

```bash
sudo pacman -S python-pipx
```

Enable the pipx binary directory:

```bash
pipx ensurepath
```

Restart your terminal after running the command above.

Clone the repository:

```bash
git clone https://github.com/<your-username>/anime-cli.git
cd anime-cli
```

Install the application:

```bash
pipx install .
```

Launch it with:

```bash
anime
```

## Development Installation

If you plan to modify the project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the application:

```bash
anime
```

## Usage

Start the player:

```bash
anime
```

On the first launch you'll be asked to choose the directory containing your anime collection. You can either:

* enter the directory path manually, or
* open a graphical folder picker and select it.

The selected directory is saved automatically and reused on future launches.

If you ever move your collection or want to use a different library, simply choose **Change anime directory** from the main menu.

A typical library structure looks like:

```text
Anime/
├── Frieren/
├── Vinland Saga/
├── Bocchi the Rock/
└── Steins;Gate/
```

## Configuration

Your selected anime library is stored in:

```text
~/.config/anime/directory.json
```

To choose a different library, either:

* select **Change anime directory** from the application menu, or
* delete the configuration file and launch `anime` again.

## Episode Naming

The built-in renamer converts filenames into the format expected by the player.

Run:

```bash
anime rename /path/to/series
```

Episodes are renamed into the following format:

```text
ep1-
ep2-
ep3-
...
```

Openings and endings are also supported:

```text
op1-
ed1-
```

## Episode Ordering

Episodes are sorted numerically instead of alphabetically.

Example:

```text
ep1-
ep2-
ep3-
...
ep10-
ep11-
```

instead of:

```text
ep1-
ep10-
ep11-
ep2-
```

## Watched Episodes

After an episode finishes playing, it is automatically marked as watched by appending:

```text
watched
```

Example:

```text
ep5-
```

becomes:

```text
ep5-watched
```

You can restore all episode names by selecting **Reset watched status** from the menu.

## Extras

If a series contains an `Extras` directory, it can be opened directly from the player.

Example:

```text
Frieren/
├── ep1-
├── ep2-
├── Extras/
│   ├── op1-
│   ├── ed1-
│   └── ep13.5-
```

Files inside `Extras` support:

* automatic sorting
* VLC playback
* watched tracking
* resetting watched status

## Project Structure

```text
anime-cli/
├── anime/
│   ├── __init__.py
│   ├── cli.py
│   ├── main.py
│   └── renamer.py
├── pyproject.toml
├── README.md
```

## License

This project is licensed under the MIT License.

