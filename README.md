
# Anime Player

A simple terminal-based anime player written in Python. It provides a curses-based interface for selecting a series and episode, launches VLC in fullscreen, and automatically keeps track of watched episodes.

## Features

* Browse your anime library from a terminal menu.
* Choose the root directory containing your anime series on first launch.
* Change the root anime directory at any time from the main menu.
* Automatically remembers your chosen directory.
* Browse episodes in numerical order.
* Supports opening an `Extras` folder for openings, endings, OVAs, or special content.
* Plays videos in **VLC** in fullscreen.
* Automatically marks watched episodes by renaming them.
* Reset watched status for an entire series or its `Extras` folder.
* Includes a built-in episode renamer.

## Requirements

* Python 3.10+
* VLC installed and available in your `PATH`
* A Unix-like operating system (Linux recommended)

## Installation

Clone the repository:

```bash
git clone https://github.com/jeff841/anime-cli.git
cd anime-cli
```

Install VLC if it is not already installed.

### Arch Linux

```bash
sudo pacman -S vlc
```

## Usage

Start the player:

```bash
python main.py
```

On the first launch, the program asks for the directory containing your anime series, for example:

```
Anime/
├── Frieren/
├── Bocchi the Rock/
├── Vinland Saga/
└── Steins;Gate/
```

The selected directory is saved and reused automatically on future launches. If you move your collection, simply select **Change anime directory** from the main menu.

### Renaming Episodes

The built-in renamer converts episode filenames into the format expected by the player.

Run:

```bash
python main.py rename /path/to/series
```

Episodes are renamed into the following format:

```
ep1-
ep2-
ep3-
...
```

The filename intentionally ends after the dash. The original file extension is removed.

## Episode Ordering

Episodes are sorted numerically rather than alphabetically.

For example:

```
ep1-
ep2-
ep3-
...
ep10-
ep11-
```

instead of:

```
ep1-
ep10-
ep11-
ep2-
```


## Watched Episodes

After an episode finishes playing, the player renames it by appending:

```
watched
```

Example:

```
ep5-
```

becomes

```
ep5-watched
```

You can restore all filenames by selecting **Reset watched status** from the menu.

## Extras

If a series contains an `Extras` directory, it can be opened from within the player. Files inside behave exactly like normal episodes:

* automatic sorting
* VLC playback
* watched tracking
* reset watched status

## Project Structure

```
.
├── main.py
├── cli.py
├── renamer.py
├── directory.json
└── README.md
```

## License

This project is released under the MIT License.

