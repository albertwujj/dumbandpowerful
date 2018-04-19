import random

# state is represented by a tuple of (player_sum, dealer_sum)
# action is represented by 0 for stick, 1 for hit

def step(state, action):
    player = state[0]
    dealer = state[1]

    if action:
        player += hit()
        if player > 21 or player < 1:
            return -1, None
        else:
            return 0, (player, dealer)
    else:
        while dealer < 17 and dealer > 0:
            dealer += hit()
        return get_reward(player, dealer), None



def hit():
    color = random.randint(0, 2)
    if color == 0:
        color == -1
    else:
        color = 1
    return random.randint(1, 10) * color


def get_reward(player, dealer):
    if dealer > 21 or dealer < 1:
        return 1
    diff = player - dealer
    if diff < 0:
        return -1
    elif diff == 0:
        return 0
    else:
        return 1

