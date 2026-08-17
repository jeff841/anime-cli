from pathlib import Path
from shutil import move


def add_series(source, collection):
    """Move a series directory into an anime collection without overwriting it."""
    if not str(source).strip():
        raise ValueError("Choose a series directory to add")
    source = Path(source).expanduser()
    collection = Path(collection).expanduser()
    if not source.is_dir():
        raise ValueError(f"Series directory does not exist: {source}")
    if not collection.is_dir():
        raise ValueError(f"Configured anime directory does not exist: {collection}")

    source = source.resolve()
    collection = collection.resolve()
    if collection in source.parents:
        raise ValueError("The series directory cannot contain the anime collection")

    destination = collection / source.name
    if destination.exists():
        raise FileExistsError(f"A series named '{source.name}' already exists in the anime directory.")

    move(str(source), str(destination))
    return destination


def move_series(series_name, collection, destination=None):
    """Move a named series out of a collection without overwriting its target."""
    collection = Path(collection).expanduser()
    destination = Path.home() if destination is None else Path(destination).expanduser()
    if not collection.is_dir():
        raise ValueError(f"Configured anime directory does not exist: {collection}")
    if not destination.is_dir():
        raise ValueError(f"Destination directory does not exist: {destination}")

    collection = collection.resolve()
    destination = destination.resolve()
    source = next(
        (
            entry for entry in collection.iterdir()
            if entry.is_dir() and entry.name.casefold() == series_name.casefold()
        ),
        None,
    )
    if source is None:
        raise ValueError(f"No series named '{series_name}' exists in the anime directory")
    source = source.resolve()
    if destination == source or destination in source.parents:
        raise ValueError("The destination directory cannot be inside the series directory")

    target = destination / source.name
    if target.exists():
        raise FileExistsError(f"A series named '{source.name}' already exists in the destination directory")

    move(str(source), str(target))
    return target
