def __init__(self, colour):

def action(self, turns):
    if action.turns === 128/SHRINK
        SHRINK += 1

    if self.phase == 'placing':
        Minimax()

        return (x,y)

    if self.phase == 'moving':

        return ((a,b),(c,d))
    else:
        return(None)

def update(self, action):





class MiniMax:
    # Max = Player
    # Min = Opponent
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.root = game_tree.root
        return

    # Given a state of the game 'game', find the best move for the Max
    # player to make
    def minimax(self, game):
        MAX_DEPTH = 4
        successors = self.get_successors(game)
        max_val = float("-inf")
        best_move = None
        for state in successors:
            curr_val = self.minimax_value(MAX_DEPTH, state, True)
            if curr_val > max_val:
                best_move = state
                max_val = curr_val
        return best_move.action

    def minimax_value(self, depth, state, alpha, beta, isMaximisingPlayer):
        if depth == 0 or self.is_terminal_state(state):
            return get_utility(state)
        else:
            if (isMaximisingPlayer):
                max_move = float("-inf")
                successors = self.get_successors(state)
                for successor in successors:
                    max_move = max(max_move, self.minimax_value(depth-1, successor, alpha, beta, !isMaximisingPlayer))
                    alpha = max(alpha, max_move)
                    if beta >= alpha:
                        return max_move
                return max_move
            else:
                min_move = float("-inf")
                successors = self.get_successors(state)
                for successor in successors:
                    min_move = min(min_move, self.minimax_value(depth-1, successor, alpha, beta, !isMaximisingPlayer)
                    beta = min(beta, min_move)
                    if beta <= alpha:
                        return min_move
                return min_move

    def max_value(self, node, alpha, beta):
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

   def min_value(self, node, alpha, beta):
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

    def get_successors(self, state):
        assert node is not None
        return node.children

    def get_utility(self, state):
        assert node is not None
        return node.utility_value

    def is_terminal_state(self, state):
        assert node is not None
        return (len(node.children) == 0)

    def EVAL(game):
        totaleval = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                totaleval = totaleval + getpiecevalue(board[i][j])
        return totaleval


    def getpiecevalue(piece, x, y):
        if piece == '-'
            return 0
