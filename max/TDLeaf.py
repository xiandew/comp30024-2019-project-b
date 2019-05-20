import json
import numpy as np
from max.max_n import eval

def get_weights():
    with open('max/weight.txt') as json_file:
        weights = json.load(json_file)
    return weights

def get_state():
    with open('max/states.json') as json_file:
        game_state = json.load(json_file)
        states = game_state['states']
        for i in range(0, len(states)):
            for colour, pieces in states[i].items():
                pieces = [tuple(p) for p in pieces ]
                states[i][colour] = pieces
        game_state['states'] = states
        return game_state

def update_weights(l, state):
    weights = get_weights()['weights']

    my_colour = state['my_colour']
    states = state['states']

    for i in range(0, len(weights)):
        w = weights[i]
        newW = w
        for i in range(0, len(weights) - 1):
            td = np.tanh(eval(states[i + 1], weights, my_colour) - eval(states[i], weights, my_colour))
            newW += ((1 / (np.cosh(eval(states[i], weights, my_colour)))) * td)
        weights[i] = newW

    with open('weight.json') as json_file:
        json.dump(weights, json_file)

def reset_states():
    with open('max/states.json', 'w') as json_file:
        initial_state = {
            "red": [[-3, 0], [-3, 1], [-3, 2], [-3, 3]], 
            "blue": [[0, 3], [1, 2], [2, 1], [3, 0]], 
            "green": [[0, -3], [1, -3], [2, -3], [3, -3]]
            }
        json.dump(initial_state, json_file)

def start_learning():
    state = get_state()
    update_weights(0, state)
    reset_states()

