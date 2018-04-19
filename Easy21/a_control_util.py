import random
import matplotlib.pyplot as plt
import numpy as np

def e_greedy(action_value, state, epsilon = 0):
    action = None
    if random.random() < epsilon:
        action = random.randint(0, 1)
    else:
        if (state, 0) in action_value and (state, 1) in action_value:
            action = 0 if action_value[(state, 0)] > action_value[(state, 1)] else 1
        else:
            if (state, 0) not in action_value:
                if (state, 1) not in action_value:
                    action = random.randint(0, 1)
                else:
                    action = 0
            else:
                action = 1
    return action

# visualize greedy policy as grid
def visualize(q, option = 'total'):
    hit_value = np.zeros((22, 12))
    stick_value = np.zeros((22, 12))
    total_value = np.zeros((22, 12))

    for i in q.keys():
        state = i[0]
        if (state, 0) in q and (state, 1) in q:
            hit_value[state] = q[(state, 1)]
            stick_value[state] = q[(state, 0)]
            total_value[state] = q[(state, 1)] - q[(state, 0)]

    hit_value = hit_value.T
    stick_value = stick_value.T
    total_value = total_value.T
    v = {
        'hit': hit_value,
        'stick': stick_value,
        'total': total_value
    }.get(option, total_value)
    plt.imshow(v, cmap='hot', interpolation='nearest')
    plt.show()

