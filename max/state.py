"""
This module is used to represent the internal game state of the Chexers game.
The state will include the locations of the pieces for each player, the number
of already exited pieces for each player, and the colour of the player.
"""

from max.utils import (get_exit_cells, moveable_cells, jumpable_cells, MOVE, JUMP, EXIT, PASS)
import json

class State:
    def __init__(self, colour):

        # Record the player's own colour
        self.colour = colour

        # Set a variable to record the number of already exited pieces
        self.num_of_exited = {
            "red": 0,
            "blue": 0,
            "green": 0
        }

        # Set the initial locations of Chexers pieces for each player
        self.piece_locs = {
            "red": [(-3, 0), (-3, 1), (-3, 2), (-3, 3)],
            "blue": [(0, 3), (1, 2), (2, 1), (3, 0)],
            "green": [(0, -3), (1, -3), (2, -3), (3, -3)]
        }

    def get_all_pieces(self):
        """
        Get the locations of all pieces on board as a single list.
        """
        return list(self.piece_locs.values())

    def get_possible_actions(self, colour):
        """
        Get all the possible actions availabe for the player with the specified
        colour.
        """

        possible_actions = []

        # Loop through all pieces of the current player
        for curr_cell in self.piece_locs[colour]:

            occupied = self.get_all_pieces()

            # Exit actions
            if curr_cell in get_exit_cells(colour):
                possible_actions += [(EXIT, curr_cell)]

            # Move actions
            for next_cell in moveable_cells(curr_cell, occupied):
                possible_actions += [(MOVE, (curr_cell, next_cell))]

            # Jump actions
            for next_cell in jumpable_cells(curr_cell, occupied):
                possible_actions += [(JUMP, (curr_cell, next_cell))]

        return possible_actions

    def update(self, colour, action):
        """
        Update the board state according to the action of the player with the
        specified colour.
        """
        (move, cells) = action
        if (move == MOVE or move == JUMP):
            (origin, dest) = cells

            # Convert the colour of the piece being jumped over to the colour of 
            # the piece that jumps over it. 
            if (move == JUMP):
                
                # The cell being jumped over
                middle_cell = tuple(map(lambda x, y: (x + y) // 2, origin, dest))
                for (piece_colour, pieces) in self.piece_locs.items():
                    if (middle_cell in pieces):
                        self.piece_locs[piece_colour].remove(middle_cell)
                        break
                self.piece_locs[colour].append(middle_cell)

            self.piece_locs[colour].remove(origin)
            self.piece_locs[colour].append(dest)

        elif (move == EXIT):
            origin = cells
            self.piece_locs[colour].remove(origin)
            self.num_of_exited[colour] += 1

    def write_to_file(self):
        """
        Write the state to the end of file that records all the game states.
        """
        with open('max/states.json') as json_file:
            states = json.load(json_file)

        states.append(self.__dict__)
        with open('max/states.json', 'w') as json_file:
            json.dump(states, json_file)
