import json
import numpy as np
from max.max_n import myeval

def get_weights():
    with open('max/weight.json') as json_file:
        weights = json.load(json_file)
    return weights

def get_states():
    with open('max/states.json') as json_file:
        states = json.load(json_file)
        for i in range(0, len(states)):
            for colour, pieces in states[i]['piece_locs'].items():
                pieces = [tuple(p) for p in pieces ]
                states[i][colour] = pieces
        return states

def update_weights(l, states):
    weights = get_weights()

    my_colour = states[0]['colour']

    for feature in list(weights.keys()):
        w = weights[feature]
        newW = w
        for j in range(0, len(states) - 1):
            td = np.tanh(myeval(states[j + 1], weights, my_colour)) - np.tanh(myeval(states[j], weights, my_colour))
            newW += ((1 / (np.cosh(myeval(states[j], weights, my_colour)))) ** 2 * td)
        weights[feature] = newW

    with open('max/weight.json', 'w') as json_file:
        json.dump(weights, json_file)

def reset_states(state):
    with open('max/states.json', 'w') as json_file:
        # initial_state = {"states": [{
        #     "red": [[-3, 0], [-3, 1], [-3, 2], [-3, 3]],
        #     "blue": [[0, 3], [1, 2], [2, 1], [3, 0]],
        #     "green": [[0, -3], [1, -3], [2, -3], [3, -3]]
        #     }]}
        json.dump([state.__dict__], json_file)

def start_learning():
    states = get_states()
    update_weights(0, states)
    # reset_states()
