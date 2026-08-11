from json import dump, load
from platformdirs import user_config_dir
from pathlib import Path
from os import path

def key(key=None):
    CONFIG_DIR = Path(user_config_dir('anime'))
    CONFIG_DIR.mkdir(parents=True,exist_ok=True)
    CONFIG_FILE = CONFIG_DIR/'api_key.json'
    CONFIG_FILE.touch(exist_ok=True)
    if key is not None and path.getsize(CONFIG_FILE.open('r+').name) == 0:
        with CONFIG_FILE.open('r+') as f:
            if path.getsize(f.name) == 0:
                data = {
                        "api_key": key
                        }
                dump(data,f)
                f.seek(0)
                data = load(f)
                return data['api_key']
    elif key is not None and path.getsize(CONFIG_FILE.open('r+').name) != 0:
        with CONFIG_FILE.open('r+') as f:
            data = load(f)
            return data['api_key']
    else:
        return


