"""
This module is used to simulate the max-n algorithm, which allows the player
to find the best action in a game with more than two players.
"""

import copy
import json
from max.utils import (PASS, exit_dist, EXIT_CELLS, get_weights)
from max.state import State

# max depth of looking ahead
max_depth = 3
colours = ["red", "green", "blue"]

def get_best_action(state):
    weights = get_weights()
    return max_n(state, 0, state.colour, weights)[1]

def get_best_state(state):
    weights = get_weights()
    return max_n(state, 0, state.colour, weights)[2]

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour, weights):
    if depth == max_depth:
        return (evaluate(state, weights), (PASS, None), None)

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)
    best_state = None

    curr_player = colours.index(colour)
    next_player = (curr_player + 1) % len(colours)

    for action in state.get_possible_actions(colour) + [(PASS, None)]:
        v = max_n(result(state, colour, action), depth + 1, colours[next_player], weights)[0]
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
            best_state = result(state, colour, action)
    return (v_max, best_action, best_state)

def result(state, colour, action):
    next_state = copy.deepcopy(state)
    next_state.update(colour, action)
    return next_state

def evaluate(state, weights):
    v = []
    for colour in colours:
        e = myeval(state, weights, colour)
        v.append(e)
    return tuple(v)

def myeval(state, weights, colour):
    if not state:
        return -float('Inf')

    piece_locs = state.piece_locs
    num_of_exited = state.num_of_exited

    total_dist = sum(exit_dist(colour, piece) + 1 for piece in piece_locs[colour])
    e = 0

    to_exit = 4 - num_of_exited[colour]
    exitable_num = len(piece_locs[colour]) - to_exit

    if (exitable_num < 0):
        to_exit = 0

    opponent_exited = sum(exited for c, exited in num_of_exited.items() if c != colour and len(piece_locs[c]) > 0)

    e = weights['total_dist'] * total_dist * -1 + weights['exitable_num'] * exitable_num + (4 - to_exit) * weights['to_exit'] + opponent_exited * weights['opponent_exited'] * -1
    return e
