from max.state import (State, MOVE, JUMP, EXIT, PASS)
from max.max_n import get_best_action

import math
import random

class ExpertPlayer:
    def __init__(self, colour):
        """
        Set up state representation.
        """
        self.state = State(colour)


    def action(self):
        """
        Decide what action to take.
        """
        possible_actions = self.state.get_possible_actions(self.state.colour)

        if (len(possible_actions) == 0):
            return (PASS, None)
        else:
            return get_best_action(self.state)


    def update(self, colour, action):
        """
        Update state representation in response to action.
        """
        self.state.update(colour, action)
