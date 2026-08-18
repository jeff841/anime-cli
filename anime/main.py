from curses import wrapper
from os import environ
from .cache import Cache
from .cli import menu
from json import dump, load
from .renamer import rename, rename_sort
from argparse import ArgumentParser
from .picture import get_picture
from re import search
from .api import AnimeAPI
from .watch_input import configured_anime_directory, watch_input
from .collection import add_series, move_series
from .show import show
from .play import play
from .reset_watched import reset_watched
from .extra import extra
from .episode import episode
import sys
from pathlib import Path
from .constants import PARSER_DESCRIPTION,ANINAME_HELP,EP_HELP,RENAME_HELP,EP_ERROR,METADATA
from .anime_details import anime_details
from .config import get_mal_client_id

def main():
    parser = ArgumentParser(description=PARSER_DESCRIPTION)
    parser.add_argument("anime_name",type=str,nargs='?',help=ANINAME_HELP)
    parser.add_argument("ep",nargs='?',type=str,help=EP_HELP)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--rename",nargs='?',const=Path('menu'),type=Path,help=RENAME_HELP)
    actions.add_argument("--add", type=Path, metavar="DIRECTORY", help="Move a series directory into the configured anime collection")
    actions.add_argument("--move", nargs='+', metavar="ARG", help="Move a collection series to [DESTINATION], defaulting to the home directory")
    args = parser.parse_args() 
    if args.rename is not None:
        if args.rename == Path('menu'):
            rename()
        else:
            rename_sort(args.rename)
        return
    if args.add is not None:
        if args.anime_name is not None or args.ep is not None:
            parser.error("--add cannot be used with an anime name or episode")
        collection = configured_anime_directory()
        if collection is None:
            parser.error("Configure an anime directory before using --add")
        try:
            destination = add_series(args.add, collection)
        except (ValueError, FileExistsError) as error:
            parser.error(str(error))
        print(f"Added {destination.name} to {collection}")
        return
    if args.move is not None:
        if args.anime_name is not None or args.ep is not None:
            parser.error("--move cannot be used with an anime name or episode")
        if not 1 <= len(args.move) <= 2:
            parser.error("--move requires SERIES and accepts at most one DESTINATION")
        collection = configured_anime_directory()
        if collection is None:
            parser.error("Configure an anime directory before using --move")
        series_name, *destination = args.move
        try:
            target = move_series(
                series_name,
                collection,
                destination[0] if destination else None,
            )
        except (ValueError, FileExistsError) as error:
            parser.error(str(error))
        print(f"Moved {series_name} to {target.parent}")
        return
    elif args.ep is not None and args.anime_name is None:
       parser.error(EP_ERROR)
    elif args.ep:
        ep = episode(args.ep)
        anime = watch_input(args.anime_name)
        choices = show(anime)
        match = search(r'\d+$',ep)
        if match:
            suffix = match.group()
            selected = int(suffix) - 1
            play(anime,choices,selected)
        else:
            print('No such episode')
            return
    else:
        anime = watch_input(args.anime_name)
        client_id = get_mal_client_id()
        cache = Cache()
        api = AnimeAPI(client_id,cache)
        if anime is None:
            return
        metadata_file, items, picture = anime_details(anime, api)
        while True:
            choices = show(anime)
            anime_choices = [entry.name for entry in anime.parent.iterdir() if entry.is_dir()]
            result = wrapper(
                menu,
                choices,
                items,
                picture,
                screen="episode",
                targets=anime_choices,
                button_start=choices.index('Get anime information'),
            )
            if result.command == 'quit':
                return
            if result.command == 'back':
                anime = watch_input()
                if anime is None:
                    return
                metadata_file, items, picture = anime_details(anime, api)
                continue
            if result.selected is None:
                continue
            if result.command == 'open_anime':
                anime = anime.parent / result.arguments[0]
                metadata_file, items, picture = anime_details(anime, api)
                continue
            if result.command == 'rename_current':
                rename_sort(anime)
                continue
            if result.command == 'rename_anime':
                rename_sort(anime.parent / result.arguments[0])
                continue
            if result.command == 'play':
                play(anime, choices, result.selected)
                continue
            if choices[result.selected] == 'Get anime information':
                query = input("Enter anime name: ").strip().lower()
                data = api.search_anime(query)
                choices2 = [anime["title"] for anime in data]
                result2 = wrapper(menu,choices2)
                if result2.command == 'quit':
                    return
                if result2.selected is None:
                    continue
                anime_id = data[result2.selected]["id"]
                metadata_file = anime/METADATA
                with metadata_file.open('w') as f:
                    dump({"id": anime_id},f)
                results = api.get_anime(anime_id)
                picture = get_picture(results["id"],results["main_picture"]["large"])
                items = [f"{results["title"]}", f"{results["synopsis"]}",f"Number of episodes: {results["num_episodes"]}",f"Rating: {results["mean"]}",f"Genres: {", ".join(genre["name"] for genre in results["genres"])}"]
                continue
            if choices[result.selected] == 'Extras':
                if extra(anime):
                    return
            if choices[result.selected] == 'Reset watched status':
                reset_watched(anime)
                continue
            if choices[result.selected] == 'Exit':
                sys.argv = [sys.argv[0]]
                return main() 
            play(anime,choices,result.selected)
    
if __name__ == '__main__':
    main()
