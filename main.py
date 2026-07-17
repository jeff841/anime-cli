from pathlib import Path
from subprocess import run

def access_dir(name):
    return Path(f'/home/jeff/Downloads/{name.lower()}/')

def choose_ep():
    ep = input("Which episode? ")
    return ep

def watch_input():
    inp = input("What do you want to watch? ")
    return inp

def play(anime,ep):
    for episode in anime.iterdir():
        if episode.name == f'ep{ep}':
            run(['cvlc', episode])
            break

def main():
    anime = watch_input()
    ep = choose_ep()
    directory = access_dir(anime)
    play(directory,ep)

if __name__ == '__main__':
    main()






