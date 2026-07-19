from curses import wrapper
from pathlib import Path
from subprocess import run
import pdb
from cli import menu

def choose_ep():
    ep = int(input("Which episode? "))
    return ep

def watch_input():
    anime_list = Path(f'/home/jeff/anime_list/')
    choices = [element.name for element in anime_list.iterdir()]
    selected = wrapper(menu,choices)
    return Path(f'/home/jeff/anime_list/{choices[selected]}')

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
        if not episode.name.endswith('watched'):
            run(['mv',str(episode),str(episode) + 'watched'])
        index += 1

def main():
    anime = watch_input()
    choices = show(anime)
    selected = wrapper(menu,choices)
    play(anime,choices,selected)
    
if __name__ == '__main__':
    main()











