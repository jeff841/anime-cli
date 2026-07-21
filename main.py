from curses import wrapper
from pathlib import Path
from subprocess import run
import pdb
from cli import menu

def watch_input():
    anime_list = Path(f'/home/jeff/anime_list/')
    choices = [element.name for element in anime_list.iterdir()]
    selected = wrapper(menu,choices)
    return Path(f'/home/jeff/anime_list/{choices[selected]}')

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
        episode = directory/episodes[index]
        if episode.name.startswith('ep'):
            run(['vlc','--fullscreen','--play-and-exit',str(episode)])
        if not episode.name.endswith('watched') and episode.name.startswith('ep'):
            episode.rename(directory / (episode.name + 'watched'))
        index += 1

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
    anime = watch_input()
    while True:
        choices = show(anime)
        selected = wrapper(menu,choices)
        if choices[selected] == 'Extras':
            extra(anime)
        if choices[selected] == 'Reset watched status':
            reset_watched(anime)
            continue
        if choices[selected] == 'Exit':
            break
        play(anime,choices,selected)
    
if __name__ == '__main__':
    main()











