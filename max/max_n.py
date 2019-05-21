"""
This module is used to simulate the max-n algorithm, which allows the player
to find the best action in a game with more than two players.
"""
import json
from max.utils import (PASS, EXIT_CELLS, TOTAL_DIST, TO_EXIT, CAN_EXIT, OPPONENT_EXITED, COLOURS,
    get_weights, evaluate, next_p, result)
from max.state import State

# max depth of looking ahead
max_depth = 3

def get_best_action(state):
    weights = get_weights()
    v, action, _ = max_n(state, 0, state.colour, weights)
    return action

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour, weights):
    if depth >= len(COLOURS):
        return (evaluate(state, weights), (PASS, None), state)

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)
    curr_player = COLOURS.index(colour)
    next_player = next_p(state, curr_player)
    best_leaf = None

    if (len(state.get_possible_actions(colour)) == 0):
        curr_player = next_p(state, curr_player)
        next_player = next_p(state, curr_player)
        colour = COLOURS[curr_player]

    for action in state.get_possible_actions(colour):
        v, _, leaf = max_n(result(state, colour, action), depth + 1, COLOURS[next_player], weights)
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
            best_leaf = leaf
    return (v_max, best_action, best_leaf)
