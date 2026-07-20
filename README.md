
# Anime Player

A simple terminal-based anime player written in Python. It provides a curses-based interface for selecting a series and episode, launches VLC in fullscreen, and automatically keeps track of watched episodes.

## Features

* Browse anime folders from a terminal menu.
* Browse episodes in numerical order.
* Play episodes in **VLC** in fullscreen.
* Automatically marks an episode as watched after playback by appending `watched` to the filename.
* Reset all watched episodes back to their original filenames from the menu.
* Uses a lightweight curses interface for keyboard navigation.

## Requirements

* Python 3
* VLC Media Player
* Linux
* A terminal that supports curses

## Directory Structure

Place each anime inside its own folder under:

```text
/home/jeff/anime_list/
```

Example:

```text
anime_list/
├── Nisekoi/
│   ├── ep1-
│   ├── ep2-
│   ├── ep3-
│   └── Extras/
├── Clannad/
│   ├── ep1-
│   └── ep2-
```

## Episode Naming

Episodes must follow this naming convention:

```text
ep1-
ep2-
ep3-
...
```

After an episode has been watched, it becomes:

```text
ep1-watched
```

The **Reset watched status** option removes the `watched` suffix from every episode in the selected series.

## Usage

Run the program:

```bash
python main.py
```

1. Select an anime.
2. Select an episode.
3. VLC launches in fullscreen.
4. When playback finishes, the episode is marked as watched.
5. Use **Reset watched status** at any time to clear all watched markers.

## Notes

* Episode files are sorted numerically regardless of the filesystem order.
* Non-episode files and folders (such as `Extras`) are listed after the numbered episodes.
* The project uses Python's `pathlib` module for filesystem operations and `curses` for the interactive interface.

## License

This project is open source and available under the MIT License.

