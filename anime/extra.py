from .show import show
from curses import wrapper
from .cli import menu
from subprocess import run
from .reset_watched import reset_watched
from .constants import EXTRAS

def extra(directory):
    directory_extra = directory/EXTRAS
    episodes_extra = show(directory_extra)
    result = wrapper(
        menu,
        episodes_extra,
        button_start=episodes_extra.index('Get anime information'),
    )
    if result.command == 'quit':
        return True
    if result.selected is None:
        return
    index_extra = result.selected
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
