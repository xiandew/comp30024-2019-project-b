from copy import deepcopy
from max.utils import (PASS, exit_dist, EXIT_CELLS)
from max.state import State

# max depth of looking ahead
max_depth = 3
colours = ["red", "green", "blue"]

def get_best_action(state):
    return max_n(state, 0, state.colour)[1]

# Inputs: state, depth, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour):
    if depth == max_depth:
        return (evaluate(state), (PASS, None))

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)

    curr_player = colours.index(colour)
    next_player = (curr_player + 1) % len(colours)

    for action in state.get_possible_actions(colour) + [(PASS, None)]:
        v = max_n(result(state, colour, action), depth + 1, colours[next_player])[0]
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
    return (v_max, best_action)

def result(state, colour, action):
    next_state = deepcopy(state)
    next_state.update(colour, action)
    return next_state

def evaluate(state):
    v = []
    for colour in colours:
        e = 0

        total_dist = sum(exit_dist(colour, piece) + 1 for piece in state.piece_locs[colour])
        to_exit = 4 - state.num_of_exited[colour]
        pieces = state.piece_locs[colour]

        # when all pieces are lost on the board
        if (total_dist == 0):
            # but no enough pieces had exited, give heavy penalty
            if (state.num_of_exited[colour] < 4):
                e = -10000
            # otherwise win
            else:
                e = 10000
        else:
            e = -1 * total_dist
            # if there are pieces on the exit cells and more than 4 pieces on board,
            # rewards the case to encourage exit action
            if ((len(set(pieces).intersection(set(EXIT_CELLS[colour]))) > 0)
                and (len(pieces) > to_exit)):
                e += 10000

        # penalty applied if the number of needing to exit less than the current
        # number of pieces, otherwise rewards are given.
        e += (len(pieces) - to_exit) * 100

        v.append(e)
    return tuple(v)
