from json import dump,load
from pathlib import Path
from platformdirs import user_config_dir

class AnimeInfo:
    def __init__(self):
        config_dir = Path(user_config_dir("anime"))
        config_dir.mkdir(parents=True,exist_ok=True)
        self.file = config_dir / "anime_info.json"
        if not self.file.exists():
            self.file.write_text("{}")
        with self.file.open('r') as f:
            self.data = load(f)
    def get(self,anime_name):
        return self.data.get(anime_name)
    def save(self,anime_name,info):
        self.data[anime_name] = info
        self._write()
    def remove(self,anime_name):
        self.data.pop(anime_name,None)
        self._write()
    def _write(self):
        with self.file.open('w') as f:
            dump(self.data,f,indent=4)
