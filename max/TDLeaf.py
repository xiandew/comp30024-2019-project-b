import json
import numpy as np
from max.max_n import myeval
from max.utils import get_weights
from max.state import dict_to_state

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

            curr_state = dict_to_state(states[j])
            curr_score = myeval(curr_state, weights, my_colour)
            next_state = dict_to_state(states[j + 1])
            next_score = myeval(next_state, weights, my_colour)

            td = np.tanh(next_score) - np.tanh(curr_score)
            newW += 10000 * ((1 / (np.cosh(curr_score))) ** 2 * td)
        weights[feature] = newW

    with open('max/weight.json', 'w') as json_file:
        json.dump(weights, json_file)

def reset_states(state):
    with open('max/states.json', 'w') as json_file:
        json.dump([state.__dict__], json_file)

def start_learning():
    states = get_states()
    update_weights(0, states)
