import copy

class MiniMax:
    '''A class that describes the minimax implementation used to find
    the 'best' move given the GameTree generated'''
    # Max = Player
    # Min = Opponent
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.currnode = game_tree.root
        return

    def minimax(self, node):
        '''Given a current game state represented by 'node', finds the best 'move'
        using a minimax approach, moves through the GameTree to this node for future
        reference, then returns the action'''
        # First, find the max utility value
        infinity = float('inf')
        best_val = self.max_value(node, -infinity, infinity)
        successors = self.get_successors(node)
        # Now find the action that brings this max utility value, assuming the opponent plays rationally,
        # and then move to the appropriate node
        best_move = None
        for elem in successors:
            # Found the correct node! So move to it and set its associated action to be our 'best' move
            if self.get_utility(elem) == best_val:
                best_move = elem.action
                self.currnode = elem
                break
        # We've moved to a new node, so have to add a layer below that node, and update utilities accordingly
        self.game_tree.add_layer(self.currnode)
        self.game_tree.update_utility(self.currnode, self.game_tree.colour)
        return best_move

    def max_value(self, node, alpha, beta):
        '''Standard minimax function that acts in the interest of the player, finding the
        maximum utility a player can attain from that particular node'''
        # No children, so get the utility value at this node and send it up
        if self.is_terminal_state(node):
            return self.get_utility(node)
        successors_states = self.get_successors(node)
        # Look at all child nodes, and find the maximum utility value, assuming
        # the opponent plays rationally, use alpha-beta pruning to ignore redundant branches
        for state in successors_states:
            alpha = max(alpha, self.min_value(state, alpha, beta))
            if alpha >= beta:
                return beta
        return alpha

    def min_value(self, node, alpha, beta):
        '''Standard minimax function that acts in the interest of the opponent, finding the
        minimum utility an opponent can attain from that particular node'''
        # Operates very similarly to 'max_value'
        if self.is_terminal_state(node):
            return self.get_utility(node)
        successor_states = self.get_successors(node)
        for state in successor_states:
            beta = min(beta, self.max_value(state, alpha, beta))
            if beta <= alpha:
                return alpha
        return beta

    def get_successors(self, node):
        assert node is not None
        return node.children.queue

    def get_utility(self, node):
        assert node is not None
        return node.utility_value

    def is_terminal_state(self, node):
        assert node is not None
        return (len(node.children.queue) == 0)
