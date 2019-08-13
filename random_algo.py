import numpy as np

def random_cpu(current_game):
    available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), current_game)
    cpu_choice = np.random.choice(available_moves)
    return cpu_choice
