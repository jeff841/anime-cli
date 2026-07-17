from pathlib import Path
from subprocess import run
import pdb

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
    for episode in episodes:
        print(episode)

def play(anime,ep):
    for episode in anime.iterdir():
        if episode.name == f'ep{ep}':
            run(['vlc','--fullscreen','--play-and-exit',episode])
            run(['mv',f'{episode}',f'{episode}watched'])
            ep += 1
            continue

def main():
    anime = watch_input()
    directory = access_dir(anime)
    show(directory)
    breakpoint()
    ep = choose_ep()
    play(directory,ep)

if __name__ == '__main__':
    main()






