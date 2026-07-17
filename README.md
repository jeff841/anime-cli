# Anime CLI

A lightweight Python command-line application for watching local anime episodes with VLC.

The program allows you to search for an anime by name, play episodes, automatically continue to the next episode, and mark completed episodes as watched.

## Features

- 🔍 Search anime by name
- ▶️ Launch episodes directly in VLC
- ⏭️ Autoplay the next episode
- ✅ Automatically mark completed episodes as watched
- 📁 Simple folder-based organization
- ⚡ Lightweight with no database or configuration required

## Requirements

- Python 3.10+
- VLC Media Player installed and available in your PATH
- Linux (tested on Arch Linux)

## Folder Structure

Place each anime inside your `~/Downloads` directory.

Example:

```
~/Downloads/
├── one piece/
│   ├── ep1-
│   ├── ep2-
│   ├── ep3-
│   └── ...
├── frieren/
│   ├── ep1-
│   ├── ep2-
│   └── ...
```

The folder name is the name you will search for inside the program.

Episodes must be named using the following format:

```
ep1-
ep2-
ep3-
...
```

Do not include spaces or other naming schemes if you want the program to find them automatically.

## Usage

Clone the repository:

```bash
git clone https://github.com/jeff841/anime-cli
cd anime-cli
```

Run the program:

```bash
python main.py
```

When prompted, enter the name of the anime folder.

Example:

```
What do you want to watch?
> frieren
```

Then choose the episode number.

## Watched Episodes

After an episode finishes playing, the program automatically marks it as watched.

## Autoplay

When an episode ends, the next episode starts automatically, allowing you to binge-watch without manually selecting each episode.

## Notes

- Anime folders must be located inside `~/Downloads`.
- Folder names determine what you search for.
- Episode filenames must follow the `ep<number>-` format.

## License

This project is open source.
