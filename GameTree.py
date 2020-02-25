from collections import defaultdict as dd
from queue import PriorityQueue
import random
import copy

BOARD_SIZE = 8
BLACK_P = "B"
WHITE_P = "W"
CORNER_P = "X"
EMPTY_P = "-"
DEAD_P = "#"
T1_LOCS = [(3,3), (4,3), (3,4), (4,4)]
T2_LOCS = [(3,2), (4,2), (5,3), (5,4), (4,5), (3,5), (2,4), (2,3)]
T3_LOCS = [(2,2), (5,5), (5,2), (2,1), (2,5), (3,1), (4,1), (5,1), (6,2), (6,3), (6,4), (6,5), (5,6), (4,6), (3,6),
(2,6), (1,5), (1,4), (1,3), (1,2)]
S1_LOCS = [(0,3), (0,4), (7,3), (7,4)]

class GameNode:
    '''A class that defines a node of the game tree, features the following
       action: The action taken to reach the GameNode
       board: The current board (game state) at the GameNode
       depth: The number of turns that have elapsed
       curr_util: The utility value of the current game state (board)
       utility_value: The utility value obtained from examining whole GameTree
       parent: The parent GameNode
       children: A priority queue of children GameNodes'''
    def __init__(self, action, board, depth, parent=None):
        self.action = action # action taken to reach game state
        self.board = board
        self.depth = depth
        self.curr_util = 0
        self.utility_value = 0
        self.parent = parent
        self.children = PriorityQueue()
        return

    def add_child(self, child):
        self.children.put(child)

    def __lt__(self, other):
        return (self.curr_util > other.curr_util)

class GameTree:
    '''A class that defines a tree of GameNodes, featuring a 'root' node,
    an empty and the colour of the player'''
    def __init__(self, colour):
        self.root = None
        # Starting game board is initialised
        board = [[EMPTY_P for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        board[0][0] = CORNER_P
        board[BOARD_SIZE-1][0] = CORNER_P
        board[0][BOARD_SIZE-1] = CORNER_P
        board[BOARD_SIZE-1][BOARD_SIZE-1] = CORNER_P
        self.root_board = board
        self.colour = colour

    def build_tree(self):
        '''Given an empty GameTree, generates a root node, as well as children
        nodes up to a depth set by MAX_DEPTH, also updates utility of all of these
        generated nodes'''
        MAX_DEPTH = 3
        # Create the root node (empty board)
        self.root = GameNode(None, self.root_board, 0)
        # Look at all possible moves, and create a sub-tree of a lower depth by 1 from
        # each of these new children nodes
        for successor in self.find_moves(self.root_board, True, self.root.depth+1):
            self.parse_subtree(successor, self.root, MAX_DEPTH-1)
        # Necessary parts of GameTree built, now update utility of each node
        self.update_utility(self.root, self.colour)

    def parse_subtree(self, successor, parent, depth):
        '''Generates a subtree of depth 'depth' from a node 'successor', attaches this 'successor' node
        to the parent node 'parent' as well'''
        # Depth > 0, so we have to add new nodes
        if depth > 0:
            # Create the new leaf node, add it as a child of its parent
            leaf_node = GameNode(successor, self.app(successor, copy.deepcopy(parent.board), parent.depth+1), parent.depth+1, parent)
            leaf_node.curr_util = self.evaluate(leaf_node.board, self.colour)
            parent.add_child(leaf_node)
            # Find all possible moves from this game state, and parse a 1 depth shallower subtree of each
            for successor in self.find_moves(leaf_node.board, (leaf_node.depth % 2 == 0), leaf_node.depth+1):
                self.parse_subtree(successor, leaf_node, depth-1)

    def update_utility(self, node, colour):
        '''Given a node 'node' and the 'colour' of the player, updates the utility_value
        of each node that has 'node' as an ancestor, ensures minimax runs correctly'''
        # No children, so evaluate the current game state and send it back up
        if (node.children.queue == []):
            node.utility_value = self.evaluate(node.board, colour)
            return node.utility_value
        # We have children, so have to check the utility value of each of them
        # and depending on the 'colour' of the player, and whose turn it is
        # figure out the optimal move for that player
        else:
            util_list = []
            successors = node.children.queue
            for successor in successors:
                util_list.append(self.update_utility(successor, colour))
            if (node.depth%2 == 0 and colour == "black"):
                node.utility_value = min(util_list)
                return min(util_list)
            elif (node.depth%2 == 0  and colour == "white"):
                node.utility_value = max(util_list)
                return max(util_list)
            elif (node.depth%2 != 0 and colour == "black"):
                node.utility_value = max(util_list)
                return max(util_list)
            else:
                node.utility_value = min(util_list)
                return min(util_list)

    def evaluate(self, board, colour):
        '''Given a current game state 'board', evaluate the position and return
        a value indicating who is in a stronger position, a higher positive value indicates
        a better position, and a lower negative value indicates a worse position'''
        player_locs = []
        player_vulnerable = dd(int)
        opp_locs = []
        opp_vulnerable = dd(int)
        value_sum = 0
        total_eval = 0
        if colour == "white":
            PLAYER_P = WHITE_P
            OPP_P = BLACK_P
        else:
            PLAYER_P = BLACK_P
            OPP_P = WHITE_P
        # Go through each of the locations on the board, check if a piece is there,
        # and depending on its location and colour, add a certain value to value_sum,
        # also add it to a list of player/opponent locations
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE):
                value_sum = value_sum + self.get_piece_value(board, col, row, colour)
                if board[col][row] == PLAYER_P:
                    player_locs.append((col, row))
                elif board[col][row] == OPP_P:
                    opp_locs.append((col, row))
        # 'Vulnerable' squares identified (pairs of opposite empty spaces around pieces),
        # we then add these squares to a dictionary
        for loc in player_locs:
            x = loc[0]
            y = loc[1]
            i = 1
            if 0<=(x-i)<=(x+i)<BOARD_SIZE:
                if board[x+i][y] != PLAYER_P:
                    if board[x-i][y] != PLAYER_P:
                        player_vulnerable[(x+i, y)]+=1
                        player_vulnerable[(x-i, y)]+=1
            if 0<=(y-i)<=(y+i)<BOARD_SIZE:
                if board[x][y+i] != PLAYER_P:
                    if board[x][y-i] != PLAYER_P:
                        player_vulnerable[(x, y+i)]+=1
                        player_vulnerable[(x, y-i)]+=1
        for loc in opp_locs:
            x = loc[0]
            y = loc[1]
            i = 1
            if 0<=(x-i)<=(x+i)<BOARD_SIZE:
                if board[x+i][y] != OPP_P:
                    if board[x-i][y] != OPP_P:
                        opp_vulnerable[(x+i, y)]+=1
                        opp_vulnerable[(x-i, y)]+=1
            if 0<=(y-i)<=(y+i)<BOARD_SIZE:
                if board[x][y+i] != OPP_P:
                    if board[x][y-i] != OPP_P:
                        opp_vulnerable[(x, y+i)]+=1
                        opp_vulnerable[(x, y-i)]+=1
        player_vul_score = 0
        opp_vul_score = 0
        # Go through each 'vulnerable' square, if an enemy piece is on it, add
        # the number associated with the square, if an enemy piece is 1 move away
        # from it, add half this number
        for key in opp_vulnerable.keys():
            x, y = key
            # Checking square itself
            if board[x][y] == PLAYER_P:
                player_vul_score += opp_vulnerable[key]
            else:
                # Checking adjacent squares and, where relevant, jumps
                for i in [-1, 1]:
                    if 0<=(x+i)<BOARD_SIZE:
                        if board[x+i][y] == PLAYER_P:
                            player_vul_score += 0.5*(opp_vulnerable[key])
                        elif board[x+i][y] == OPP_P:
                            if 0<=(x+i+i)<BOARD_SIZE:
                                if board[x+i+i][y] == PLAYER_P:
                                    player_vul_score += 0.5*(opp_vulnerable[key])
                    if 0<=(y+i)<BOARD_SIZE:
                        if board[x][y+i] == PLAYER_P:
                            player_vul_score += 0.5*(opp_vulnerable[key])
                        elif board[x][y+i] == OPP_P:
                            if 0<=(y+i+i)<BOARD_SIZE:
                                if board[x][y+i+i] == PLAYER_P:
                                    player_vul_score += 0.5*(opp_vulnerable[key])
        for key in player_vulnerable.keys():
            x, y = key
            if board[x][y] == OPP_P:
                opp_vul_score += player_vulnerable[key]
            else:
                for i in [-1, 1]:
                    if 0<=(x+i)<BOARD_SIZE:
                        if board[x+i][y] == OPP_P:
                            opp_vul_score += 0.5*(player_vulnerable[key])
                        elif board[x+i][y] == PLAYER_P:
                            if 0<=(x+i+i)<BOARD_SIZE:
                                if board[x+i+i][y] == OPP_P:
                                    opp_vul_score += 0.5*(player_vulnerable[key])
                    if 0<=(y+i)<BOARD_SIZE:
                        if board[x][y+i] == OPP_P:
                            opp_vul_score += 0.5*(player_vulnerable[key])
                        elif board[x][y+i] == PLAYER_P:
                            if 0<=(y+i+i)<BOARD_SIZE:
                                if board[x][y+i+i] == PLAYER_P:
                                    opp_vul_score += 0.5*(player_vulnerable[key])
        total_eval = 0.6*(len(player_locs)-len(opp_locs))+0.3*value_sum+0.1*(player_vul_score-opp_vul_score)
        return total_eval

    def get_piece_value(self, board, x, y, colour):
        '''Given a location of a piece on the board, (x,y), look at its centrality
        and assign it a 'value' based on this'''
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
            # Most to least central
            if pos in T1_LOCS:
                pos_val = 1
            elif pos in T2_LOCS:
                pos_val = 0.75
            elif pos in T3_LOCS:
                pos_val = 0.5
            elif pos in S1_LOCS:
                pos_val = 0.4
            else:
                pos_val = 0.25
        # If its an opposing piece, make this value negative
        if board[x][y] == OPP_P:
            pos_val = -pos_val
        return pos_val

    def app(self, successor, board, turn):
        '''Given a board and an action 'successor', applies the action to the board
        and returns the new board, includes mechanisms to handle shrinking of board
        and potential capturing'''
        if turn % 2 == 0:
            PLAYER_P = BLACK_P
            OPP_P = WHITE_P
        else:
            PLAYER_P = WHITE_P
            OPP_P = BLACK_P
        # Board is shrinking! So will have to handle things differently
        if (turn-24)%64 == 0 and (turn-24)//64 > 1:
            # No action made, so just kill outer squares, add new corners, and
            # check if any captures have occurred due to these new corners
            if not successor:
                shrink = (turn-88)//64
                # Shrink the board
                for i in range(BOARD_SIZE):
                    board[shrink-1][i] = DEAD_P
                    board[i][shrink-1] = DEAD_P
                    board[i][BOARD_SIZE-shrink] = DEAD_P
                    board[BOARD_SIZE-shrink][i] = DEAD_P
                # New corner locations
                board[shrink][shrink] = CORNER_P
                board[shrink][BOARD_SIZE-shrink-1] = CORNER_P
                board[BOARD_SIZE-shrink-1][shrink] = CORNER_P
                board[BOARD_SIZE-shrink-1][BOARD_SIZE-shrink-1] = CORNER_P
                # Look at all corner positions in appropriate order, and see if captures have occurred
                for col, row in [(shrink, shrink), (shrink, BOARD_SIZE-shrink-1), (BOARD_SIZE-shrink-1, BOARD_SIZE-shrink-1), (BOARD_SIZE-shrink-1, shrink)]:
                        for i in [-1, 1]:
                            if board[col+i][row] in [PLAYER_P, OPP_P]:
                                if board[col+i+i][row] in [PLAYER_P, OPP_P] and board[col+i+i][row] != board[col+i][row]:
                                    board[col+i][row] = EMPTY_P
                            if board[col][row+i] in [PLAYER_P, OPP_P]:
                                if board[col][row+i+i] in [PLAYER_P, OPP_P] and board[col][row+i+i] != board[col][row+i]:
                                    board[col][row+i] = EMPTY_P
                return board
            # An action made, so perform the action, check for captures on the old board, shrink the board,
            # and then check again for captures with the new corners
            else:
                # Perform the action
                board[successor[0][0]][successor[0][1]] = EMPTY_P
                board[successor[1][0]][successor[1][1]] = PLAYER_P
                # Checking to see if a capture has been made with that move
                for i in [-1, 1]:
                    if 0<=(successor[1][0]+i+i)<BOARD_SIZE:
                        if board[successor[1][0]+i][successor[1][1]] == OPP_P:
                            if board[successor[1][0]+i+i][successor[1][1]] in [PLAYER_P, CORNER_P]:
                                board[successor[1][0]+i][successor[1][1]] = EMPTY_P
                    if 0<=(successor[1][1]+i+i)<BOARD_SIZE:
                        if board[successor[1][0]][successor[1][1]+i] == OPP_P:
                            if board[successor[1][0]][successor[1][1]+i+i] in [PLAYER_P, CORNER_P]:
                                board[successor[1][0]][successor[1][1]+i] = EMPTY_P
                i = 1
                # Checking if the piece has committed suicide
                if 0<=(successor[1][0]-i)<(successor[1][0]+i)<BOARD_SIZE:
                    if board[successor[1][0]+i][successor[1][1]] in [OPP_P, CORNER_P] and board[successor[1][0]-i][successor[1][1]] in [OPP_P, CORNER_P]:
                        board[successor[1][0]][successor[1][1]] = EMPTY_P
                if 0<=(successor[1][1]-i)<(successor[1][1]+i)<BOARD_SIZE:
                    if board[successor[1][0]][successor[1][1]+i] in [OPP_P, CORNER_P] and board[successor[1][0]][successor[1][1]-i] in [OPP_P, CORNER_P]:
                        board[successor[1][0]][successor[1][1]] = EMPTY_P
                # Shrinking the board appropriately
                shrink = (turn-88)//64
                for i in range(BOARD_SIZE):
                    board[shrink-1][i] = DEAD_P
                    board[i][shrink-1] = DEAD_P
                    board[i][BOARD_SIZE-shrink] = DEAD_P
                    board[BOARD_SIZE-shrink][i] = DEAD_P
                board[shrink][shrink] = CORNER_P
                board[shrink][BOARD_SIZE-shrink-1] = CORNER_P
                board[BOARD_SIZE-shrink-1][shrink] = CORNER_P
                board[BOARD_SIZE-shrink-1][BOARD_SIZE-shrink-1] = CORNER_P
                # Checking for captures with the new corners
                for col, row in [(shrink, shrink), (shrink, BOARD_SIZE-shrink-1), (BOARD_SIZE-shrink-1, BOARD_SIZE-shrink-1), (BOARD_SIZE-shrink-1, shrink)]:
                        for i in [-1, 1]:
                            if board[col+i][row] in [PLAYER_P, OPP_P]:
                                if board[col+i+i][row] in [PLAYER_P, OPP_P] and board[col+i+i][row] != board[col+i][row]:
                                    board[col+i][row] = EMPTY_P
                            if board[col][row+i] in [PLAYER_P, OPP_P]:
                                if board[col][row+i+i] in [PLAYER_P, OPP_P] and board[col][row+i+i] != board[col][row+i]:
                                    board[col][row+i] = EMPTY_P
        # The board does not change this turn
        else:
            # No action, so just return the same board
            if not successor:
                return board
            # This is placing place, so just put the piece there and check for captures
            elif isinstance(successor[0], int):
                board[successor[0]][successor[1]] = PLAYER_P
                for i in [-1, 1]:
                    if 0<=(successor[0]+i+i)<BOARD_SIZE:
                        if board[successor[0]+i][successor[1]] == OPP_P:
                            if board[successor[0]+i+i][successor[1]] in [PLAYER_P, CORNER_P]:
                                board[successor[0]+i][successor[1]] = EMPTY_P
                    if 0<=(successor[1]+i+i)<BOARD_SIZE:
                        if board[successor[0]][successor[1]+i] == OPP_P:
                            if board[successor[0]][successor[1]+i+i] in [PLAYER_P, CORNER_P]:
                                board[successor[0]][successor[1]+i] = EMPTY_P
                if 0<=(successor[0]-i)<(successor[0]+i)<BOARD_SIZE:
                    if board[successor[0]+i][successor[1]] in [OPP_P, CORNER_P] and board[successor[0]-i][successor[1]] in [OPP_P, CORNER_P]:
                        board[successor[0]][successor[1]] = EMPTY_P
                if 0<=(successor[1]-i)<(successor[1]+i)<BOARD_SIZE:
                    if board[successor[0]][successor[1]+i] in [OPP_P, CORNER_P] and board[successor[0]][successor[1]-i] in [OPP_P, CORNER_P]:
                        board[successor[0]][successor[1]] = EMPTY_P
            # This is moving phase, so perform a movement, then check for captures
            else:
                board[successor[0][0]][successor[0][1]] = EMPTY_P
                board[successor[1][0]][successor[1][1]] = PLAYER_P
                for i in [-1, 1]:
                    if 0<=(successor[1][0]+i+i)<BOARD_SIZE:
                        if board[successor[1][0]+i][successor[1][1]] == OPP_P:
                            if board[successor[1][0]+i+i][successor[1][1]] in [PLAYER_P, CORNER_P]:
                                board[successor[1][0]+i][successor[1][1]] = EMPTY_P
                    if 0<=(successor[1][1]+i+i)<BOARD_SIZE:
                        if board[successor[1][0]][successor[1][1]+i] == OPP_P:
                            if board[successor[1][0]][successor[1][1]+i+i] in [PLAYER_P, CORNER_P]:
                                board[successor[1][0]][successor[1][1]+i] = EMPTY_P
                i = 1
                if 0<=(successor[1][0]-i)<(successor[1][0]+i)<BOARD_SIZE:
                    if board[successor[1][0]+i][successor[1][1]] in [OPP_P, CORNER_P] and board[successor[1][0]-i][successor[1][1]] in [OPP_P, CORNER_P]:
                        board[successor[1][0]][successor[1][1]] = EMPTY_P
                if 0<=(successor[1][1]-i)<(successor[1][1]+i)<BOARD_SIZE:
                    if board[successor[1][0]][successor[1][1]+i] in [OPP_P, CORNER_P] and board[successor[1][0]][successor[1][1]-i] in [OPP_P, CORNER_P]:
                        board[successor[1][0]][successor[1][1]] = EMPTY_P
        return board

    def add_layer(self, node):
        ''' Given a node, find all of the terminal nodes that have 'node' as an ancestor,
        and add another layer of children nodes to each of these terminal nodes'''
        # No children, so add a layer here
        if node.children.queue == []:
            for successor in self.find_moves(node.board, (node.depth % 2 == 0), node.depth+1):
                self.parse_subtree(successor, node, 1)
        # Has children, so have to keep searching deeper
        else:
            for successor in node.children.queue:
                self.add_layer(successor)

    def find_moves(self, board, isWhite, turn):
        '''Given a current board configuration, the the colour of the player
        whose turn it is, return a list of all of the possible actions the player
        can take, if no action is possible, return the forfeit move None'''
        moves = dd(list)
        out_moves = []
        if isWhite:
            PLAYER_CHAR = WHITE_P
            OPP_CHAR = BLACK_P
        else:
            PLAYER_CHAR = BLACK_P
            OPP_CHAR = WHITE_P
        # Movement phase
        if (turn > 24):
            # If the board has been shrunk, we need only scan certain parts of the
            # board for pieces
            shrink = (turn-88)//64
            if (shrink < 0):
                shrink = 0
            i = 0
            if (turn-24)%64 != 0:
                max_r = 4-shrink
            elif (turn == 88):
                max_r = 4-shrink
            else:
                max_r = 4-shrink+1
            for i in range(max_r):
                for row in [3-i,4+i]:
                    for col in range(BOARD_SIZE):
                        # Found a player character
                        if board[row][col] == PLAYER_CHAR:
                            for i in [-1,1]:
                                # Checking if there are horizontal moves possible
                                if 0+shrink<=(row+i)<BOARD_SIZE-shrink:
                                    # Spot is unoccupied, so the move is valid
                                    if board[row+i][col] == EMPTY_P:
                                        moves[(row, col)].append((row+i, col))
                                    # Spot is occupied, so have to check if we can jump
                                    elif board[row+i][col] == PLAYER_CHAR or board[row+i][col] == OPP_CHAR:
                                        if 0+shrink<=(row+i+i)<BOARD_SIZE-shrink:
                                            # We can, so the move is valid
                                            if board[row+i+i][col] == EMPTY_P:
                                                moves[(row, col)].append((row+i+i, col))
                                # Checking if there are vertical moves possible
                                if 0+shrink<=(col+i)<BOARD_SIZE-shrink:
                                    # Spot is unoccupied, so move is valid
                                    if board[row][col+i] == EMPTY_P:
                                        moves[(row, col)].append((row, col+i))
                                    # Checking if we can jump as before
                                    elif board[row][col+i] == PLAYER_CHAR or board[row][col+i] == OPP_CHAR:
                                        if 0+shrink<=(col+i+i)<BOARD_SIZE-shrink:
                                            if board[row][col+i+i] == EMPTY_P:
                                                moves[(row, col)].append((row, col+i+i))
            for key, value in moves.items():
                for val in value:
                    out_moves.append((key, val))
            if (len(out_moves) == 0):
                out_moves.append(None)
        # Placing phase
        else:
            # Set ranges based on the valid locations each colour can place
            if isWhite:
                row_range = [0, 6]
            else:
                row_range = [2, 8]
            for i in range(4):
                for col in [3-i, 4+i]:
                    for row in range(row_range[0], row_range[1]):
                        # Empty here, so we can make a move here
                        if board[col][row] == EMPTY_P:
                            out_moves.append((col, row))
        return out_moves
