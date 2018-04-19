from main import step
import random
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
from linear_model import LinApproximator

# Sarsa Lambda with value approximation

def e_greedy(q, state, epsilon = 0.05):
    x_0 = get_feature_vec(state, 0)
    x_1 = get_feature_vec(state, 1)
    action = None
    if random.random() < epsilon:
        return random.randint(0, 1)
    else:
        return 0 if q(x_0) > q(x_1) else 1

def get_feature_vec(state, action):
    x = np.zeros(36)

    # make sum start from 0
    player = state[0] - 1
    dealer = state[1] - 1

    dealer_poses = []
    dealer_pos = dealer // 3
    if dealer < 9:
        dealer_poses.append(dealer_pos)
    # add overlap
    if dealer == 3 or dealer == 6 or dealer == 9:
        dealer_poses.append(dealer_pos - 1)

    player_poses = []
    player_pos = player // 3
    if player < 18:
        player_poses.append(player_pos)
    # add overlap
    if player_pos > 0:
        player_poses.append(player_pos - 1)

    for i in range(len(dealer_poses)):
        for j in range(len(player_poses)):
            activated = action * 18 + dealer_poses[i] * 6 + player_poses[j]
            x[activated] = 1
    return x


random.seed()
visited_count = {}
av_count = {}
q = {}
e_trace = np.zeros(36)
n0 = 100
lambd = .1
epsilon = .05
q = LinApproximator()

eps = 0
while eps < 100000:

    state = (random.randint(1, 10), random.randint(1, 10))
    action = e_greedy(q, state, epsilon)
    while True:
        visited = visited_count[state] if state in visited_count else 0
        epsilon = n0 / (n0 + visited)

        sa = (state, action)
        x = get_feature_vec(state, action)

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

        # update eligibility traces vector
        e_trace = lambd * e_trace + x


        # execute action
        reward, next_state = step(state, action)

        q_next = 0
        if next_state is not None:
            # sample next action from policy
            next_action = e_greedy(q, next_state, epsilon)
            sa_next = (next_state, next_action)
            x_next = get_feature_vec(next_state, next_action)
            q_next = q(x_next)

        # calc td target
        alpha = 1 / (av_count[sa])
        target = reward + q_next - q(x)

        # update values: td lambda backwards view, w/ function approximation
        q.tdl_step(target, e_trace)

        if next_state is None:
            break
        else:
            state = next_state
            action = next_action
        eps += 1

policy_arr = np.zeros((11, 21))

for i in range(10):
    for j in range(20):
        for k in range(1):
            hit = get_feature_vec((j + 1, i + 1), 1)
            stick = get_feature_vec((j + 1, i + 1), 0)
            policy_arr[i,j] = (q(hit) - q(stick)) * 2


plt.imshow(policy_arr, cmap='hot', interpolation='nearest')
plt.show()