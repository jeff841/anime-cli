from .constants import METADATA

def show(anime):
    episodes = [ep.name for ep in anime.iterdir() if ep.name != METADATA]
    episodes.append("Get anime information")
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

