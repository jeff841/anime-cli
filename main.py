from curses import wrapper
from pathlib import Path
from subprocess import run
import pdb
from cli import menu

def access_dir(name):
    return Path(f'/home/jeff/Downloads/{name.lower()}/')

def choose_ep():
    ep = int(input("Which episode? "))
    return ep

def watch_input():
    inp = input("What do you want to watch? ")
    return inp

def show(anime):
    episodes = [ep.name for ep in anime.iterdir()] 
    episodes.sort(
            key=lambda name: (
                not name.startswith('ep'),
                int(name[2:name.index('-')]) if name.startswith('ep') else float('inf')
                )
            )
    return episodes

def play(directory,episodes, index):
    while index < len(episodes):
        episode = directory/episodes[index]
        run(['vlc','--fullscreen','--play-and-exit',str(episode)])
        if not episode.name.endswith('WATCHED'):
            run(['mv',str(episode),str(episode) + 'WATCHED'])
        index += 1

def main():
    anime = watch_input()
    directory = access_dir(anime)
    choices = show(directory)
    selected = wrapper(menu,choices)
    play(directory,choices,selected)
    
if __name__ == '__main__':
    main()






