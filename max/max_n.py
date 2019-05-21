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
    v, action, _ = max_n(state, 0, state.colour, weights)
    print(v)
    return action

def write_best_leaf(state, colour):
    weights = get_weights()
    _, _, best_leaf = max_n(state, 0, colour, weights)
    best_leaf.write_to_file()    

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour, weights):
    if depth >= len(colours):
        return (evaluate(state, weights), (PASS, None), state)

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)
    curr_player = colours.index(colour)
    next_player = next_p(state, curr_player)
    best_leaf = None

    if (len(state.get_possible_actions(colour)) == 0):
        curr_player = next_p(state, curr_player)
        next_player = next_p(state, curr_player)
        colour = colours[curr_player]
  
    for action in state.get_possible_actions(colour):
        v, _, leaf = max_n(result(state, colour, action), depth + 1, colours[next_player], weights)
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
            best_leaf = leaf
    return (v_max, best_action, best_leaf)

def next_p(state, curr_player):
    next_player = curr_player + 1 
    while(1):
        next_player %= 3
        if len(state.piece_locs[colours[next_player]]) > 0:
            break
        next_player += 1
    return next_player

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

    e = 0

    # The sum of the distance between each piece to the exit cell
    total_dist = sum(exit_dist(colour, piece) + 1 for piece in piece_locs[colour])

    e += weights['total_dist'] * total_dist * -1

    # The number of pieces on board
    # e += weights['num_of_pieces'] * len(piece_locs[colour])

    # The number of pieces that need to exit to win the game
    to_exit = 4 - num_of_exited[colour]

    # Whether the player has enough pieces to win the game. If there is not
    # enough pieces, can_exit will be negative. Else, it will non-negative
    can_exit = len(piece_locs[colour]) - to_exit

    if (can_exit < 0):
        to_exit = 0

    e += to_exit * weights['to_exit'] * -1

    e += can_exit * weights['can_exit']

    # The sum of the number of exited pieces for our opponents. If the player
    # deosn't have enough pieces to win the game, that player will be ignored.
    opponent_exited = sum(exited for c, exited in num_of_exited.items() if c != colour and len(piece_locs[c]) > 0)

    e += opponent_exited * weights['opponent_exited'] * -1

    # e = weights['total_dist'] * total_dist * -1 + weights['exitable_num'] * exitable_num + (4 - to_exit) * weights['to_exit'] + opponent_exited * weights['opponent_exited'] * -1
    return e
