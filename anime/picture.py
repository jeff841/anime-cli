from pathlib import Path
from requests import get
from platformdirs import user_cache_dir
from .constants import CONFIG,PIC_DIR

PICTURE_DIR = Path(user_cache_dir(CONFIG))/PIC_DIR

def get_picture(anime_id,url):
    PICTURE_DIR.mkdir(parents=True, exist_ok=True)
    picture = PICTURE_DIR/f"{anime_id}.jpg"
    if not picture.exists():
        response = get(url)
        response.raise_for_status()
        picture.write_bytes(response.content)
    return picture
