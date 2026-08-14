from pathlib import Path
from platformdirs import user_config_dir
from os import path
from .constants import CONFIG,ANIME_DIR,NOT_DIR,EXPLORER_DIR,DIR_STRUCTURE
from .cli import menu
from curses import wrapper
from tkinter import Tk,filedialog
from json import dump,load

def watch_input(anime_name=None):
    CONFIG_DIR = Path(user_config_dir(CONFIG))
    CONFIG_DIR.mkdir(parents=True,exist_ok=True)
    CONFIG_FILE = CONFIG_DIR/ANIME_DIR
    CONFIG_FILE.touch(exist_ok=True)
    with CONFIG_FILE.open('r+') as f:
        if path.getsize(f.name) == 0:
            choicesd = ["Enter the directory where your series folders are located","Open file explorer","Exit"]
            selectedd = wrapper(menu,choicesd)
            if choicesd[selectedd] == 'Enter the directory where your series folders are located':
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
            elif choicesd[selectedd] == 'Open file explorer':
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
        choices = [element.name for element in directory.iterdir()]
        choices.append('Change anime directory')
        choices.append('Exit')
        selected = wrapper(menu,choices)
        if choices[selected] == 'Change anime directory':
            CONFIG_FILE.write_text('')
            return watch_input()
        elif choices[selected] == 'Exit':
            return
        else:
            return Path(directory/choices[selected])

