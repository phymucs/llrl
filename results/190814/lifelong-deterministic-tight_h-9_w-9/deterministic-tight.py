"""
Lifelong RL experiment in constant transition function setting
"""

import numpy as np

from llrl.agents.rmax import RMax
from llrl.agents.lrmax import LRMax
from llrl.agents.maxqinit import MaxQInit
from llrl.agents.lrmaxqinit import LRMaxQInit
from llrl.utils.env_handler import make_env_distribution
from llrl.experiments import run_agents_lifelong


def experiment():
    # Parameters
    gamma = .9
    env_distribution = make_env_distribution(env_class='deterministic-tight', env_name='deterministic-tight',
                                             gamma=gamma)
    actions = env_distribution.get_actions()
    n_known = 10
    p_min = 1. / 7.  # There are seven possible MDPs
    epsilon_q = .1
    epsilon_m = .01
    delta = .1
    r_max = 1.
    v_max = 1.
    n_states = 4
    max_mem = 10

    # Agents
    rmax = RMax(actions=actions, gamma=gamma, r_max=r_max, v_max=v_max, deduce_v_max=False, n_known=n_known,
                deduce_n_known=False, epsilon_q=epsilon_q, epsilon_m=epsilon_m, name='RMax')
    lrmax = LRMax(actions=actions, gamma=gamma, r_max=r_max, v_max=v_max, deduce_v_max=False, n_known=n_known,
                  deduce_n_known=False, epsilon_q=epsilon_q, epsilon_m=epsilon_m, delta=delta, n_states=n_states,
                  max_memory_size=max_mem, prior=None, estimate_distances_online=True,
                  min_sampling_probability=p_min, name='LRMax')
    lrmaxprior = LRMax(actions=actions, gamma=gamma, r_max=r_max, v_max=v_max, deduce_v_max=False, n_known=n_known,
                       deduce_n_known=False, epsilon_q=epsilon_q, epsilon_m=epsilon_m, delta=delta, n_states=n_states,
                       max_memory_size=max_mem, prior=0.1, estimate_distances_online=True,
                       min_sampling_probability=p_min, name='LRMax(Dmax=0.1)')
    maxqinit = MaxQInit(actions=actions, gamma=gamma, r_max=r_max, v_max=v_max, deduce_v_max=False, n_known=n_known,
                        deduce_n_known=False, epsilon_q=epsilon_q, epsilon_m=epsilon_m, delta=delta, n_states=n_states,
                        min_sampling_probability=p_min, name='MaxQInit')
    lrmaxqinit = LRMaxQInit(actions=actions, gamma=gamma, r_max=r_max, v_max=v_max, deduce_v_max=False, n_known=n_known,
                            deduce_n_known=False, epsilon_q=epsilon_q, epsilon_m=epsilon_m, delta=delta,
                            n_states=n_states, max_memory_size=max_mem, prior=None, estimate_distances_online=True,
                            min_sampling_probability=p_min, name='LRMaxQInit')
    agents_pool = [rmax, lrmax, lrmaxprior, maxqinit, lrmaxqinit]

    # Run
    run_agents_lifelong(agents_pool, env_distribution, n_instances=5, n_tasks=50, n_episodes=50, n_steps=100,
                        reset_at_terminal=False, plot_only=False, open_plot=True, plot_title=True)


if __name__ == '__main__':
    np.random.seed(1993)
    experiment()