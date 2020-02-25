def EVAL(game):
    totaleval = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            totaleval = totaleval + getpiecevalue(board[i][j], i, j, self)
    return totaleval

def getpiecevalue(piece, x, y, self):
    #evaluate piece out of 100
    if piece == '-':
        return 0
    if piece == 'X':
        return 0
    if piece == OPP_CHAR:
        #look for piece being capturable
        for i in [-1,1]:
            if board[x+i][y] == PLAYER_CHAR:
                if board[x-i][y] == PLAYER_CHAR:
                    return 80
            if board[x][y+i] == PLAYER_CHAR:
                if board[x][y-i] == PLAYER_CHAR:
                    return 80
    if piece == PLAYER_CHAR:
        #avoid being captured
        for i in [-1,1]:
            if board[x+i][y] == OPP_CHAR:
                if board[x-i][y] == OPP_CHAR:
                    return -80
            if board[x][y+i] == OPP_CHAR:
                if board[x][y-i] == OPP_CHAR:
                    return -80
        #placing adjecent to opponent
        if self.phase == 'placing':
                if board[x-1][y-1] == OPP_CHAR:
                    return 20
                if board[x-1][y+1] == OPP_CHAR:
                    return 20
                if board[x+1][y-1] == OPP_CHAR:
                    return 20
                if board[x+1][y+1] == OPP_CHAR:
                    return 20
        #promote pairing and centred
        for i in [-1,1]:
            if board[x+i][y] == PLAYER_CHAR:
                if y == 3 or y == 4:
                    return 30
                elif:
                    return 20
            if board[x][y+i] == PLAYER_CHAR:
                if y == 3 or y == 4:
                    return 30
                elif:
                    return 20
        #avoid being next to corner
        if x == 6 and (y == 0 or y == 7):
            return -50
        if x == 1 and (y == 0 or y == 7):
            return -50
        if x == 0 and (y == 1 or y == 6):
            return -50
        if x == 7 and (y == 1 or y == 6):
            return -50



def get_piece_value(self, board, x, y, colour):
    # Evaluate piece out of 100
    if colour == "white":
        PLAYER_P = WHITE_P
        OPP_P = BLACK_P
    else:
        PLAYER_P = BLACK_P
        OPP_P = WHITE_P
    if board[x][y] in [CORNER_P, EMPTY_P]:
        return 0
    else:
        # Centre Control
        pos_val = 0
        pos = (x, y)
        if pos in T1_LOCS:
            pos_val = 100
        elif pos in S1_LOCS:
            pos_val = 50
        elif pos in T2_LOCS:
            pos_val = 50
        else:
            pos_val = 25
        #for i in [-1,1]:
        #    if (x+i) < BOARD_SIZE and (x+i) > 0:
        #        if board[x+i][y] == OPP_P:
        #            pos_val = 60
        #    if (y+i) < BOARD_SIZE and (y+i) > 0:
        #        if board[x][y+i] == OPP_P:
        #            pos_val = 60
    if board[x][y] == OPP_P:
        pos_val = -pos_val
    return pos_val

class MiniMax:
    # Max = Player
    # Min = Opponent
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.currnode = game_tree.root
        return

    def minimax(self, node):
        # first, find the max value
        best_val = self.max_value(node) # should be root node of tree
        # second, find the node which HAS that max value
        #  --> means we need to propagate the values back up the
        #      tree as part of our minimax algorithm
        successors = self.get_successors(node)
        # find the node with our best move
        best_move = None

        for elem in successors:   # ---> Need to propagate values up tree for this to work
            if self.get_utility(elem) == best_val:
                best_move = elem.action
                self.currnode = elem
                break
            # return that best value that we've found
        self.game_tree.add_layer(self.currnode, 4)
        self.game_tree.update_utility(self.currnode, self.game_tree.colour, self.game_tree.root_board)
        return best_move

    def max_value(self, node):
        if self.is_terminal_state(node):
            return self.get_utility(node)
        infinity = float('inf')
        max_value = -infinity

        successors_states = self.get_successors(node)
        for state in successors_states:
            max_value = max(max_value, self.min_value(state))
        return max_value

    def min_value(self, node):
        if self.is_terminal_state(node):
            return self.get_utility(node)
        infinity = float('inf')
        min_value = infinity

        successor_states = self.get_successors(node)
        for state in successor_states:
            min_value = min(min_value, self.max_value(state))
        return min_value


def max_value(self, node):
   if self.is_terminal_state(node):
       return self.get_utility(node)
   if node.depth == MAX_DEPTH:
        return EVAL(node)
   infinity = float('inf')
   max_value = -infinity
   alpha = max_value

   successors_states = self.get_successors(node)
   for state in successors_states:
       alpha = max(alpha, self.min_value(state))
       if alpha >= beta:
           return beta
   return alpha

def min_value(self, node):
    if self.is_terminal_state(node):
       return self.get_utility(node)
    if node.depth == MAX_DEPTH:
        return EVAL(node)
    infinity = float('inf')
    min_value = infinity
    beta = min_value

    successor_states = self.get_successors(node)
    for state in successor_states:
        beta = min(beta, self.max_value(state))
        if beta <= alpha:
            return alpha
    return beta





import os, sys, getopt, pdb



class TD(object):

    def __init__(self, nstates, alpha, gamma, ld, init_val = 0.0):
        self.V = np.ones(nstates) * init_val
        self.e = np.zeros(nstates)
        self.nstates = nstates
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount
        self.ld = ld # lambda

def value(self, state):
        return self.V[state]

    def delta(self, pstate, reward, state):
        """
        This is the core error calculation. Note that if the value
        function is perfectly accurate then this returns zero since by
        definition value(pstate) = gamma * value(state) + reward.
        """
        return reward + (self.gamma * self.value(state)) - self.value(pstate)

    def train(self, pstate, reward, state):
        """
        A single step of reinforcement learning.
        """

        delta = self.delta(pstate, reward, state)

        self.e[pstate] += 1.0

        #for s in range(self.nstates):
        self.V += self.alpha * delta * self.e
        self.e *= (self.gamma * self.ld)

        return delta

    def learn(self, nepisodes, env, policy, verbose = True):
        # learn for niters episodes with resets
        for i in range(nepisodes):
            self.reset()
            t = env.single_episode(policy) # includes env reset
            for (previous, action, reward, state, next_action) in t:
                self.train(previous, reward, state)
            if verbose:
                print i

    def reset(self):
        self.e = np.zeros(self.nstates)
