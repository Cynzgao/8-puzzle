from __future__ import division
from __future__ import print_function

import sys
import math
import time
#import queue as Q
from heapq import heappush, heappop

import resource


## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])


    def swap(self, swap_ind):
        new_config = self.config[:]
        new_config[self.blank_index] = new_config[swap_ind]
        new_config[swap_ind] = 0
        return new_config


    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index >= 3):
            new = self.swap(self.blank_index - 3)
            return PuzzleState(new, self.n, parent=self, action="Up", cost=self.cost+1)
        return None

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index < 3*2):
            new = self.swap(self.blank_index + 3)
            return PuzzleState(new, self.n, parent=self, action="Down", cost=self.cost+1)
        return None

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index % 3 > 0):
            new = self.swap(self.blank_index-1)
            return PuzzleState(new, self.n, parent=self, action="Left", cost=self.cost+1)
        return None


    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if ((self.blank_index + 1) % 3 != 0):
            new = self.swap(self.blank_index + 1)
            return PuzzleState(new, self.n, parent=self, action="Right", cost=self.cost+1)
        return None

    def expand(self):
        """ Generate the child nodes of this node """
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


    # add less than in case need to compare puzzleState object
    def __lt__(self, other):
        return 0
