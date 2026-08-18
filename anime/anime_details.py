from .constants import METADATA
from json import load
from .picture import get_picture

def anime_details(anime, api):
    """Load the optional metadata used beside an anime's episode menu."""
    metadata_file = anime / METADATA
    metadata_file.touch(exist_ok=True)
    if metadata_file.stat().st_size == 0:
        return metadata_file, None, None

    with metadata_file.open() as f:
        metadata = load(f)
    results = api.get_anime(metadata["id"])
    picture = get_picture(results["id"], results["main_picture"]["large"])
    items = [f"{results["title"]}", f"{results["synopsis"]}",f"Number of episodes: {results["num_episodes"]}",f"Rating: {results["mean"]}",f"Genres: {", ".join(genre["name"] for genre in results["genres"])}"]
    return metadata_file, items, picture

