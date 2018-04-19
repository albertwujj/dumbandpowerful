from main import step
import random
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
from a_control_util import e_greedy, visualize

# Sarsa Lambda

random.seed()
visited_count = {}
av_count = {}
q = {}
e_trace = {}
n0 = 100
lambd = .1

eps = 0
while eps < 20000:


    state = (random.randint(1, 10), random.randint(1, 10))
    while True:
        visited = visited_count[state] if state in visited_count else 0
        epsilon = n0 / (n0 + visited)

        action = e_greedy(q, state, epsilon)
        sa = (state, action)

        # count the state-action visit
        if sa in av_count:
            av_count[sa] += 1
        else:
            av_count[sa] = 1

        # count the state visit
        if state in visited_count:
            visited_count[state] += 1
        else:
            visited_count[state] = 1

        # update eligibility traces
        for i in e_trace.keys():
            e_trace[i] = lambd * e_trace[i]
        if sa not in e_trace:
            e_trace[sa] = 1
        else:
            e_trace[sa] += 1

        # execute action
        reward, next_state = step(state, action)

        # sample next action from policy
        next_action = e_greedy(q, next_state, epsilon)
        sa_next = (next_state, next_action)

        #calc td target
        if sa not in q:
            q[sa] = 0
        if sa_next not in q:
            q[sa_next] = 0
        target = reward + q[sa_next] - q[sa]

        # update values: td lambda backwards view
        alpha = 1 / (av_count[sa])
        for i in e_trace.keys():
            q[i] += alpha * e_trace[i] * target

        if next_state is None:
            break
        else:
            state = next_state
        eps += 1

visualize(q, 'stick')
