from MiniMax import MiniMax
from GameTree import GameTree
import copy

BOARD_SIZE = 8
BLACK_P = "B"
WHITE_P = "W"
CORNER_P = "X"
EMPTY_P = "-"

class Player:
    '''This class defines the Player, providing the capacity to make a move,
    as well as update internal data structures (GameTree and MiniMax) with
    information regarding a move an opponent has made'''
    def __init__(self, colour):
        self.colour = colour
        if colour == "white":
            self.p = WHITE_P
            self.opp_p = BLACK_P
        else:
            self.p = BLACK_P
            self.opp_p = WHITE_P
        # Contains a GameTree and MiniMax object, one for storing the game tree,
        # the other for using the tree to find optimal moves
        self.game_tree = GameTree(self.colour)
        self.game_tree.build_tree()
        self.minimax = MiniMax(self.game_tree)
        self.phase = "P"
        return

    def action(self, turn):
        '''Given the turn number 'turn', returns an action to perform based on
        the current game state and the GameTree using MiniMax'''
        # Movement phase, so add 24 to the turn value, this is done for simplicity in GameTree
        if self.phase == "M":
            turn += 24
        # Last placement phase, so have to change phase to 'M'
        if (23<=turn<=24 and self.phase == "P"):
            self.phase = "M"
        # Return the minimax result from the current game state
        return self.minimax.minimax(self.minimax.currnode)

    def update(self, action):
        '''Given an 'action' that has been performed by an opponent, updates
        the GameTree and MiniMax objects accordingly'''
        for successor in self.minimax.get_successors(self.minimax.currnode):
            # This is the action the opponent took, so move to this node
            if successor.action == action:
                self.minimax.currnode = successor
                # Node movement, so have to add a layer and update utilities
                self.minimax.game_tree.add_layer(self.minimax.currnode)
                self.minimax.game_tree.update_utility(self.minimax.currnode, self.colour)
        return
