import copy
from max.utils import (PASS, exit_dist, EXIT_CELLS)
from max.state import State
import json

# max depth of looking ahead
max_depth = 3
colours = ["red", "green", "blue"]
curr_state = None

def get_best_action(state):
    global curr_state
    curr_state = state
    with open('max/weight.json') as json_file:
        weights = json.load(json_file)
    return max_n(state, 0, state.colour, weights['weights'])[1]

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour, weights):
    if depth == max_depth:
        return (evaluate(state, weights), (PASS, None))

    # 3 dimensions
    v_max = (-99999, -99999, -99999)
    best_action = (PASS, None)

    curr_player = colours.index(colour)
    next_player = curr_player + 1
    while(1):
        next_player %= len(colours)
        if (len(curr_state.piece_locs[colours[next_player]]) > 0):
            break
        next_player += 1

    for action in state.get_possible_actions(colour):
        v = max_n(result(state, colour, action), depth + 1, colours[next_player], weights)[0]
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
    return (v_max, best_action)

def result(state, colour, action):
    next_state = copy.deepcopy(state)
    next_state.update(colour, action)
    return next_state

def evaluate(state, weights):
    v = []
    for colour in colours:
        # e = 0

        # total_dist = sum(exit_dist(colour, piece) + 1 for piece in state.piece_locs[colour])

        # # when all pieces are lost on the board
        # if (total_dist == 0):
        #     # but no enough pieces had exited, give heavy penalty
        #     if (state.num_of_exited[colour] < 4):
        #         e = -10000
        #     # otherwise win
        #     else:
        #         e = 10000
        # else:
        #     e = -1 * total_dist
        #     # if there are pieces on the exit cells and more than 4 pieces on board,
        #     # rewards the case to encourage exit action
        #     if ((len(set(state.piece_locs[colour]).intersection(set(EXIT_CELLS[colour]))) > 0)
        #         and (len(state.piece_locs[colour]) > (4 - state.num_of_exited[colour]))):
        #         e += 10000

        # # penalty applied if the number of needing to exit less than the current
        # # number of pieces, otherwise rewards are given.
        # e += (len(state.piece_locs[colour]) - (4 - state.num_of_exited)) * 100

        e = eval(state, weights, colour)

        v.append(e)
    return tuple(v)

def eval(state, weights, colour):
    total_dist = sum(exit_dist(colour, piece) + 1 for piece in state.piece_locs[colour])
    e = 0

    e = weights[0] * total_dist
    return e