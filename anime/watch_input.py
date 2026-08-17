from pathlib import Path
from platformdirs import user_config_dir
from os import path
from .constants import CONFIG,ANIME_DIR,NOT_DIR,EXPLORER_DIR,DIR_STRUCTURE
from .commands import episode_index, first_unwatched_episode
from .cli import menu
from .collection import add_series, move_series
from .play import play
from .renamer import rename_sort
from .show import show
from curses import wrapper
from tkinter import Tk,filedialog
from json import dump,load


def configured_anime_directory():
    """Return the configured anime collection directory, if one exists."""
    config_dir = Path(user_config_dir(CONFIG))
    config_file = config_dir / ANIME_DIR
    if not config_file.is_file() or config_file.stat().st_size == 0:
        return None
    with config_file.open() as f:
        return Path(load(f)["anime_list"])


def watch_input(anime_name=None):
    CONFIG_DIR = Path(user_config_dir(CONFIG))
    CONFIG_DIR.mkdir(parents=True,exist_ok=True)
    CONFIG_FILE = CONFIG_DIR/ANIME_DIR
    CONFIG_FILE.touch(exist_ok=True)
    with CONFIG_FILE.open('r+') as f:
        if path.getsize(f.name) == 0:
            choicesd = ["Enter the directory where your series folders are located","Open file explorer","Exit"]
            result = wrapper(menu,choicesd)
            if result.command == 'quit' or result.selected is None:
                return
            if choicesd[result.selected] == 'Enter the directory where your series folders are located':
                while True:
                    inp = input("Directory: ").strip()
                    d = Path(inp).expanduser()
                    if not d.is_dir():
                        print(NOT_DIR)
                        continue
                    if not all(cont.is_dir() for cont in d.iterdir()):
                        print(DIR_STRUCTURE)
                        continue
                    break
            elif choicesd[result.selected] == 'Open file explorer':
                root = Tk()
                root.withdraw()
                folder = filedialog.askdirectory(title=EXPLORER_DIR)
                d = folder
                dpath = Path(d)
                for cont in dpath.iterdir():
                    if not cont.is_dir():
                        print(DIR_STRUCTURE)
                        return watch_input()
            else:
                return
            data = {
                    "anime_list": str(d)                   
                    }
            dump(data,f)
        else:
            data = load(f)
        directory = Path(data["anime_list"])
        if anime_name is not None:
            for series in directory.iterdir():
                if series.name.lower() == anime_name.lower():
                    return series
        anime_choices = [element.name for element in directory.iterdir() if element.is_dir()]
        choices = anime_choices.copy()
        choices.append('Add series')
        choices.append('Change anime directory')
        choices.append('Exit')
        result = wrapper(
            menu,
            choices,
            screen="anime",
            targets=anime_choices,
            click_commands={'Add series': 'add_from_picker'},
            button_start=len(anime_choices),
        )
        if result.command == 'quit':
            return
        if result.command == 'add_series':
            try:
                destination = add_series(result.arguments[0], directory)
            except (ValueError, FileExistsError) as error:
                print(error)
            else:
                print(f"Added {destination.name} to {directory}")
            return watch_input()
        if result.command == 'move_series':
            try:
                target = move_series(
                    result.arguments[0],
                    directory,
                    result.arguments[1] if len(result.arguments) > 1 else None,
                )
            except (ValueError, FileExistsError) as error:
                print(error)
            else:
                print(f"Moved {result.arguments[0]} to {target.parent}")
            return watch_input()
        if result.command == 'add_from_picker' or (
            result.selected is not None and choices[result.selected] == 'Add series'
        ):
            root = Tk()
            root.withdraw()
            source = filedialog.askdirectory(title="Select series directory")
            if source:
                try:
                    destination = add_series(source, directory)
                except (ValueError, FileExistsError) as error:
                    print(error)
                else:
                    print(f"Added {destination.name} to {directory}")
            return watch_input()
        if result.selected is None:
            return
        if result.command == 'play':
            anime = directory / choices[result.selected]
            episodes = show(anime)
            selected_episode = (
                episode_index(episodes, result.arguments[0])
                if result.arguments
                else first_unwatched_episode(episodes)
            )
            if selected_episode is not None:
                play(anime, episodes, selected_episode)
            return watch_input()
        if result.command == 'rename_anime':
            rename_sort(directory / result.arguments[0])
            return watch_input()
        if choices[result.selected] == 'Change anime directory':
            CONFIG_FILE.write_text('')
            return watch_input()
        elif choices[result.selected] == 'Exit':
            return
        else:
            return Path(directory/choices[result.selected])
