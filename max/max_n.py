import copy
from max.utils import PASS
from max.state import State

# max depth of looking ahead
max_depth = 3
colours = ["red", "green", "blue"]

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour):
    if depth == max_depth:
        return (evaluate(state), (PASS, None))

    # 3 dimensions
    v_max = (-1, -1, -1)
    best_action = (PASS, None)

    curr_player = colours.index(colour)
    next_player = (curr_player + 1) % len(colours)

    for action in state.get_possible_actions(colour):
        v = max_n(result(state, colour, action), depth + 1, colours[next_player])[0]
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action

    return (v_max, best_action)

def result(state, colour, action):
    next_state = copy.deepcopy(state)
    next_state.update(colour, action)
    return next_state

def evaluate(state):
    v = []
    for colour in colours:
        # The shortest distance towards the exit cells.
        total_dist = 12 * 6 - sum(state.exit_dist(piece) + 5 for piece in state.piece_locs[colour])

        # The number of pieces on board
        piece_num = len(state.get_pieces(colour))
        if (state.num_of_exited < 4):
            #TODO 

        v.append(total_dist + piece_num)
    return tuple(v)
