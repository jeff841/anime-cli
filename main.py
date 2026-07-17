from pathlib import Path
from subprocess import run
import shutil
import pdb

def access_dir(name):
    anime = Path(f'/home/jeff/Downloads/{name.lower()}/')
    return anime

def choose_ep():
    ep = input("Which episode? ")
    return ep

def watch_input():
    inp = input("What do you want to watch? ")
    return inp

def play(anime,ep,name):
    for episode in anime:
        if r'\d' in episode == ep and int(ep) < 10:
            with open('/home/jeff/.local/bin/vlcrun.txt','w+') as file:
                file.write(f'vlc /home/jeff/Downloads/{name.lower()}/ep{ep}')
                run(['chmod', '+x', f'{file}'])
                run(f'{file}')
                break

def main():
    anime = watch_input()
    ep = choose_ep()
    directory = access_dir(anime)
    play(directory,ep,anime)

if __name__ == '__main__':
    main()






