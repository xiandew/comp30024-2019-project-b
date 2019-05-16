from max.utils import (moveable_cells, jumpable_cells, MOVE, JUMP, EXIT, PASS)

# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green": [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

class State:
    def __init__(self, colour):

        # Record the player's own colour
        self.colour = colour

        # Set a variable to record the number of already exited pieces
        self.num_of_exited = 0

        # Set the initial locations of Chexers pieces for each player
        self.piece_locs = {
                            "red": [(-3, 0), (-3, 1), (-3, 2), (-3, 3)],
                            "blue": [(0, 3), (1, 2), (2, 1), (3, 0)],
                            "green": [(0, -3), (1, -3), (2, -3), (3, -3)]
                        }


    def get_pieces(self, colour):
        """
        Get a player's own Chexers' pieces.
        """
        return self.piece_locs[colour]

    def get_other_pieces(self):
        """
        Get other players' Chexer pieces locations
        """
        other_pieces = []
        for (colour, pieces) in self.piece_locs.items():
            if (colour != self.colour):
                other_pieces += pieces
        return other_pieces

    def get_all_pieces(self):
        occupied = []
        for pieces in self.piece_locs.values():
            occupied += pieces
        return occupied

    def get_exit_cells(self):
        """
        Get a player's own exit cells.
        """
        return EXIT_CELLS[self.colour]

    def get_possible_actions(self, colour):
        possible_actions = []

        # Loop through all pieces of the current player
        for curr_cell in self.get_pieces(colour):

            occupied = self.get_all_pieces()

            # Exit actions
            if curr_cell in self.get_exit_cells():
                possible_actions += [(EXIT, curr_cell)]

            # Move actions
            for next_cell in moveable_cells(curr_cell, occupied):
                possible_actions += [(MOVE, (curr_cell, next_cell))]

            # Jump actions
            for next_cell in jumpable_cells(curr_cell, occupied):
                possible_actions += [(JUMP, (curr_cell, next_cell))]

        return possible_actions

    def exit_dist(self, qr):
        """
        how many hexes away from a coordinate is the nearest exiting hex?
        Reference from sample solution for part A
        """
        q, r = qr
        if self.colour == 'red':
            return 3 - q
        if self.colour == 'green':
            return 3 - r
        if self.colour == 'blue':
            return 3 - (-q-r)

    def update(self, colour, action):
        """
        Update the board state according to the action of the player with the
        specified colour.
        """
        (move, cells) = action
        if (move == MOVE or move == JUMP):
            (origin, dest) = cells

            if (move == JUMP):
                # Convert the captured piece to another colour accordingly
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
