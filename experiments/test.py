from llrl.envs.gridworld import GridWorld
from llrl.algorithms.dynamic_programming import dynamic_programming
from llrl.envs.handler import Handler
import numpy as np


def print_state_distances(d):
    n = d.shape[0]
    assert n == d.shape[1]
    diag = np.zeros(shape=n)
    for i in range(n):
        diag[i] = d[i, i]
    print('distances :', diag)
    print('max       :', diag.max())


def wasserstein_mdp_distance_test():
    # Parameters
    h = Handler()
    m1 = GridWorld(map_name='maze1', is_slippery=False)
    m2 = GridWorld(map_name='maze2', is_slippery=False)
    m3 = GridWorld(map_name='maze3', is_slippery=False)
    gamma = 0.9

    # Compute
    v1 = dynamic_programming(m1, gamma=gamma, threshold=1e-10, iter_max=1000, verbose=False)
    v2 = dynamic_programming(m2, gamma=gamma, threshold=1e-10, iter_max=1000, verbose=False)

    state_distances = h.bi_simulation_distance(m1, m2)
    distance_m1_m2 = h.wasserstein_mdp_distance(m1, m2, state_distances)
    lipschitz_constant = (float(m1.nS) / (h.cr * (1.0 - gamma)))
    gap = lipschitz_constant * distance_m1_m2

    upper_bounds = np.array(v1, dtype=float)
    for i in range(len(upper_bounds)):
        upper_bounds[i] += gap

    # Display
    print('Display environments')
    m1.render()
    m2.render()
    print('Value function 1        :')
    m1.display_to_m(v1)
    print('Value function 2        :')
    m1.display_to_m(v2)
    print('Difference between both :')
    m1.display_to_m(abs(v1 - v2))
    print()
    print('Distance between states :\n', state_distances)
    print('Distance between MDPs d = ', distance_m1_m2)
    print('Lipschitz constant    K = ', lipschitz_constant)
    print('Gap               K * d = ', gap)
    print('Upper-bounds for MDP 2  :')
    m1.display_to_m(upper_bounds)


def best_match_transfer(v_source, match_matrix, lipschitz_constant, distance):
    ns = len(v_source)
    upper_bound = np.zeros(shape=v_source.shape, dtype=float)
    for i in range(ns):
        for j in range(ns):
            if match_matrix[i, j] == 1:
                upper_bound[i] = v_source[j]
    upper_bound += lipschitz_constant * distance
    return upper_bound


def best_match_mdp_distance_test():
    # Parameters
    h = Handler()
    m1 = GridWorld(map_name='maze1', is_slippery=False)
    m2 = GridWorld(map_name='maze2', is_slippery=False)
    gamma = 0.9

    # Compute
    distance_m1_m2, match_m1_m2 = h.best_match_mdp_distance(m1, m2)
    lipschitz_constant = 1.0 / (h.cr * (1.0 - gamma))

    v1 = dynamic_programming(m1, gamma=gamma, threshold=1e-10, iter_max=1000, verbose=False)
    v2 = dynamic_programming(m2, gamma=gamma, threshold=1e-10, iter_max=1000, verbose=False)

    # Display
    print('Display environments')
    m1.render()
    m2.render()
    print('Value function 1        :')
    m1.display_to_m(v1)
    print('Value function 2        :')
    m1.display_to_m(v2)
    print('Difference between both :')
    m1.display_to_m(abs(v1 - v2))
    print('match m1, m2            :\n', match_m1_m2)
    print('lipschitz constant      :', lipschitz_constant)
    print('distance                :', distance_m1_m2)
    print('Transferred upper-bound from m1 to m2:')
    print(best_match_transfer(v1, match_m1_m2, lipschitz_constant, distance_m1_m2))


if __name__ == "__main__":
    # wasserstein_mdp_distance_test()
    best_match_mdp_distance_test()
