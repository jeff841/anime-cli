def reset_watched(directory):
    for episode in directory.iterdir():
        if episode.name.endswith('watched'):
            new_name = directory/episode.name.removesuffix('watched')
            episode.rename(new_name)

