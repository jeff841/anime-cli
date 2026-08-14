from curses import wrapper
from .cli import menu
from json import dump, load
from .renamer import rename, rename_sort
from argparse import ArgumentParser
from .picture import get_picture
from re import search
from .api import AnimeAPI
from .watch_input import watch_input
from .show import show
from .play import play
from .reset_watched import reset_watched
from .extra import extra
from .episode import episode
import sys
from pathlib import Path
from .constants import PARSER_DESCRIPTION,ANINAME_HELP,EP_HELP,RENAME_HELP,EP_ERROR,METADATA,API_URL

def main():
    parser = ArgumentParser(description=PARSER_DESCRIPTION)
    parser.add_argument("anime_name",type=str,nargs='?',help=ANINAME_HELP)
    parser.add_argument("ep",nargs='?',type=str,help=EP_HELP)
    parser.add_argument("--rename",nargs='?',const=Path('menu'),type=Path,help=RENAME_HELP)
    args = parser.parse_args() 
    if args.rename is not None:
        if args.rename == Path('menu'):
            rename()
        else:
            rename_sort(args.rename)
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
        items = None
        picture = None
        api = AnimeAPI(API_URL)
        if anime is None:
            return
        metadata_file = anime/METADATA
        metadata_file.touch(exist_ok=True)
        if metadata_file.stat().st_size > 0:
            with metadata_file.open() as f:
                metadata = load(f)
            results = api.get_anime(metadata["id"])
            picture = get_picture(results["id"],results["main_picture"]["large"])
            items = [results["title"],results["synopsis"],", ".join(genre["name"] for genre in results["genres"])]
        while True:
            choices = show(anime)
            selected = wrapper(menu,choices,items,picture)
            if choices[selected] == 'Get anime information':
                query = input("Enter anime name: ").strip().lower()
                data = api.search_anime(query)
                choices2 = [anime["title"] for anime in data]
                selected2 = wrapper(menu,choices2)
                anime_id = data[selected2]["id"]
                metadata_file = anime/"anime.json"
                with metadata_file.open('w') as f:
                    dump({"id": anime_id},f)
                results = api.get_anime(anime_id)
                picture = get_picture(results["id"],results["main_picture"]["large"])
                items = [results["title"], results["synopsis"],", ".join(genre["name"] for genre in results["genres"])]
                continue
            if choices[selected] == 'Extras':
                extra(anime)
            if choices[selected] == 'Reset watched status':
                reset_watched(anime)
                continue
            if choices[selected] == 'Exit':
                sys.argv = [sys.argv[0]]
                return main() 
            play(anime,choices,selected)
    
if __name__ == '__main__':
    main()











