from shutil import which
from subprocess import run

def play(directory,episodes,index):
    VLC = which('vlc') or which('vlc.exe')
    if VLC is None:
        raise RuntimeError("VLC is not installed or is not in PATH")
    while index < len(episodes):
        if directory is not None:
            episode = directory/episodes[index]
            if episode.name.startswith('ep'):
                run([VLC,'--fullscreen','--play-and-exit',str(episode)])
            if not episode.name.endswith('watched') and episode.name.startswith('ep'):
                episode.rename(directory / (episode.name + 'watched'))
            index += 1
        else:
            return

