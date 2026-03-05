density_history = []

def update_density_timeline(density):

    density_history.append(density)

    if len(density_history) > 50:
        density_history.pop(0)

    return density_history
