from curses import wrapper
from pathlib import Path
from os import path
from subprocess import run
import pdb
from cli import menu
from json import dump, load
from renamer import rename
from argparse import ArgumentParser

def watch_input():
    with open("/home/jeff/git_projects/anime/directory.json", 'r+') as f:
        if path.getsize(f.name) == 0:
            data = {
                    "anime_list": input("Enter the directory where your episode files are located: ")                    
                    }
            dump(data,f)
        else:
            data = load(f)
        directory = Path(data["anime_list"])
        choices = [element.name for element in directory.iterdir()]
        choices.append('Change anime directory')
        choices.append('Exit')
        selected = wrapper(menu,choices)
        if choices[selected] == 'Change anime directory':
            run(['rm',f'{f.name}'])
            run(['touch','/home/jeff/git_projects/anime/directory.json'])
            watch_input()
        if choices[selected] == 'Exit':
            return
        return Path(f'{directory}/{choices[selected]}')
            
def show(anime):
    episodes = [ep.name for ep in anime.iterdir()] 
    episodes.sort(
            key=lambda name: (
                not name.startswith(('ep','op','ed')),
                int(name[2:name.index('-')]) if name.startswith(('ep','op','ed')) else float('inf')
                )
            )
    episodes.sort(
            key = lambda name: (
                not name.startswith('op')
                )
            )
    episodes.append('Reset watched status')
    episodes.append('Exit')
    return episodes

def play(directory,episodes,index):
    while index < len(episodes):
        if directory is not None:
            episode = directory/episodes[index]
            if episode.name.startswith('ep'):
                run(['vlc','--fullscreen','--play-and-exit',str(episode)])
            if not episode.name.endswith('watched') and episode.name.startswith('ep'):
                episode.rename(directory / (episode.name + 'watched'))
            index += 1
        else:
            return

def reset_watched(directory):
    for episode in directory.iterdir():
        if episode.name.endswith('watched'):
            new_name = directory/episode.name.removesuffix('watched')
            episode.rename(new_name)

def extra(directory):
    directory_extra = directory/'Extras'
    episodes_extra = show(directory_extra)
    index_extra = wrapper(menu,episodes_extra)
    while index_extra < len(episodes_extra):
        episode = directory_extra/episodes_extra[index_extra]
        if episode.name.startswith(('ep','op','ed')):
            run(['vlc','--fullscreen','--play-and-exit',str(episode)])
        if not episode.name.endswith('watched') and episode.name.startswith(('ep','op','ed')):
            episode.rename(directory_extra/(episode.name + 'watched'))
        if episodes_extra[index_extra] == 'Reset watched status':
            reset_watched(directory_extra)
            extra(directory)
        if episodes_extra[index_extra] == 'Exit':
            return
        index_extra += 1

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    rename_parser = subparsers.add_parser("rename")
    rename_parser.add_argument("directory",type=Path)
    args = parser.parse_args()
    if args.command == "rename":
        rename(args.directory)
    else:
        anime = watch_input()
        if anime is None:
            return
        while True:
            choices = show(anime)
            selected = wrapper(menu,choices)
            if choices[selected] == 'Extras':
                extra(anime)
            if choices[selected] == 'Reset watched status':
                reset_watched(anime)
                continue
            if choices[selected] == 'Exit':
                anime = None
                main()
            play(anime,choices,selected)
    
if __name__ == '__main__':
    main()











