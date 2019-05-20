"""
This module handles the interaction between the player and the referee, so that
an aciton will be chosen to be played when the game proceeds to this player's
turn.
"""

import math
import random

from max.state import (State, PASS)
from max.max_n import get_best_action
from max.TDLeaf import (reset_states, start_learning)

class MaxnPlayer:
    def __init__(self, colour):
        """
        Initialise the game state, and reset the file that records the game
        state.
        """
        self.state = State(colour)
        reset_states(self.state)


    def action(self):
        """
        Return the best action among all possible actions according to the
        current game state
        """

        possible_actions = self.state.get_possible_actions(self.state.colour)

        if (len(possible_actions) == 0):
            return (PASS, None)
        else:
            return get_best_action(self.state)


    def update(self, colour, action):
        """
        Update the game state, and append the current game state to the end of
        all game states recorded. In addition, update the set of weights as long
        as the game is not over.
        """
        self.state.update(colour, action)
        self.state.write_to_file()
        start_learning()
