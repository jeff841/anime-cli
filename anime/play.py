from shutil import which
from subprocess import run
from .constants import VLC_ERROR

def play(directory,episodes,index):
    VLC = which('vlc') or which('vlc.exe')
    if VLC is None:
        raise RuntimeError(VLC_ERROR)
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

