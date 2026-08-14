from pathlib import Path
from platformdirs import user_config_dir
from os import path
from .cli import menu
from curses import wrapper
from tkinter import Tk,filedialog
from json import dump,load

def watch_input(anime_name=None):
    CONFIG_DIR = Path(user_config_dir('anime'))
    CONFIG_DIR.mkdir(parents=True,exist_ok=True)
    CONFIG_FILE = CONFIG_DIR/'directory.json'
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
                        print("This directory does not exist.")
                        continue
                    if not all(cont.is_dir() for cont in d.iterdir()):
                        print(
                            "Select the directory in which you store your series folders.\n"
                            "The structure should be:\n"
                            "./\n"
                            "    anime1/\n"
                            "        ep1-\n"
                            "        ep2-\n"
                            "        ...\n"
                            "    anime2/\n"
                            "        ep1-\n"
                            "        ep2-\n"
                            "        ..."
                        )
                        continue
                    break
            elif choicesd[selectedd] == 'Open file explorer':
                root = Tk()
                root.withdraw()
                folder = filedialog.askdirectory(title='Select your directory')
                d = folder
                dpath = Path(d)
                for cont in dpath.iterdir():
                    if not cont.is_dir():
                        print("Select the directory in which you store your series folders. The structure should be: \n./\n    anime1/\n        ep1-\n        ep2-\n        ...\n    anime2/\n        ep1-\n        ep2-\n        ...")
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

