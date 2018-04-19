from main import step
import random
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
from a_control_util import e_greedy, visualize

# Monte-Carlo Control

random.seed()

visited_count = {}
av_count = {}
q = {}
curr_g = {}
n0 = 100

eps = 0
while eps < 1000:


    state = (random.randint(1, 10), random.randint(1, 10))
    while True:

        visited = visited_count[state] if state in visited_count else 0
        epsilon = n0 / (n0 + visited)

        # count the state visit
        if state in visited_count:
            visited_count[state] += 1
        else:
            visited_count[state] = 1

        # choose action
        action = e_greedy(q, state, epsilon)

        # execute action, update curr total return counts
        reward, next_state = step(state, action)
        if (state,action) not in curr_g:
            curr_g[(state, action)] = 0
        for i in curr_g.keys():
            curr_g[i] += reward

        if next_state is None:
            break
        else:
            state = next_state

    # update value function
    for i in curr_g.keys():
        # count the state-action visit
        if i in av_count:
            av_count[i] += 1
        else:
            av_count[i] = 1

        alpha = 1/(av_count[i])
        if i not in q:
            q[i] = curr_g[i]
        else:
            q[i] += alpha * (curr_g[i] - q[i])
    eps += 1
    curr_g = {}

print(q)

#visualize greedy policy as grid
visualize(q)

