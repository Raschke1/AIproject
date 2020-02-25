from collections import defaultdict as dd
import sys

UNOCCUPIED_CHAR = "-"
CORNER_CHAR = "X"
WHITE_CHAR = "O"
BLACK_CHAR = "@"
BOARD_SIZE = 8


# Find number of valid moves for a particular player given a board state
def findMoves(board, isWhite):
    moves = dd(list)
    nMoves = 0
    if isWhite:
        PLAYER_CHAR = WHITE_CHAR
        OPP_CHAR = BLACK_CHAR
    else:
        PLAYER_CHAR = BLACK_CHAR
        OPP_CHAR = WHITE_CHAR
    # Look at all of the board locations that won't cause indexing problems
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Found a player character
            if board[row][col] == PLAYER_CHAR:
                for i in [-1,1]:
                    if 0<=(row+i)<BOARD_SIZE:
                        if board[row+i][col] == UNOCCUPIED_CHAR:
                            moves[(row, col)].append((row+i, col))
                            nMoves += 1
                        elif board[row+i][col] == PLAYER_CHAR or board[row+i][col] == OPP_CHAR:
                            if 0<=(row+i+i)<BOARD_SIZE:
                                if board[row+i+i][col] == UNOCCUPIED_CHAR:
                                    moves[(row, col)].append((row+i+i, col))
                                    nMoves += 1
                    if 0<=(col+i)<BOARD_SIZE:
                        if board[row][col+i] == UNOCCUPIED_CHAR:
                            moves[(row, col)].append((row, col+i))
                            nMoves += 1
                        elif board[row][col+i] == PLAYER_CHAR or board[row][col+i] == OPP_CHAR:
                            if 0<=(col+i+i)<BOARD_SIZE:
                                if board[row][col+i+i] == UNOCCUPIED_CHAR:
                                    moves[(row, col)].append((row, col+i+i))
                                    nMoves += 1
    return [moves, nMoves]

def massacre(board):
    VALID_MOVES = findMoves(board, True)[0]
    MOVES = []
    WHITE_1 = (-1,-1)
    WHITE_2 = (-1,-1)
    FROM = (0,0)
    TO = (0,0)
	GOAL_x = -1
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == BLACK_CHAR:
                #search for nearest 2 WHITE_CHAR
                i = row
                j = col
                n = 1
				#Check for corner position
				if (row = 0 and col = 1) or (row = 1 and col = 0):
					WHITE_1 = (0,0)
				if (row = 0 and col  = 7) or (row = 1 and col = 8):
					WHITE_1 = (0,8)
				if (row = 7 and col = 0) or (row = 1 and col = 8):
					WHITE_1 = (8,0)
				if (row = 7 and col = 8) or (row = 8 and col = 7):
					WHITE_1 = (8,8)

                while WHITE_2 == (-1,-1):
                    for x in range (-n,n+1):
                        for y in range (-n,n+1):
                            if board[i+x][j+y] == WHITE_CHAR:
                                if WHITE_1 == (-1,-1):
                                    W1_x = i+x
                                    W2_y = j+y
                                    WHITE_1 = (W1_x,W2_y)
                                else:
                                    W2_x = i+x
                                    W2_y = j+y
                                    WHITE_2 = (W2_x,W2_y)
                        break
                    n += 1

	            #move white 1 to BLACK_CHAR
	            while board[row][col] == BLACK_CHAR:

					if (W1_x == row and (col == W1_y+1 or col == W1_y-1) or
						W1_y == col and (row == W1_x+1 or row == W1_x-1)):
						#select goal position
						GOAL_x = row - (row - W1_x)
						GOAL_y = col - (col - W1_y)

					if GOAL_x == -1:
		                FROM_1 = (W1_x, W1_y)
		                if W1_x - row > 1:
		                    W1_x -= 1
		                elif W1_x - row < -1:
		                    W1_x += 1
		                elif W1_y - col > 1:
		                    W1_y -= 1
		                elif W1_y - col < -1:
		                    W1_y += 1
		                TO_1 = (W1_x, W1_y)
		                MOVES.append((FROM_1, TO_1))
		                print("{}->{}".format(FROM_1, TO_1))

					if GOAL_x != -1:
		                FROM_2 = (W2_x, W2_y)
		                if W2_x - GOAL_x > 0:
		                    W2_x -= 1
		                elif W2_x - GOAL_x < 0:
		                    W2_x += 1
		                elif W2_y - GOAL_y > 0:
		                    W2_y -= 1
		                elif W2_y - GOAL_y < 0:
		                    W2_y += 1
		                TO_2 = (W2_x, W2_y)
		                print("{}->{}".format(FROM_2, TO_2))
		                MOVES.append((FROM_2, TO_2))

	                #eliminate BLACK_CHAR
	                if row == W2_x:
	                    if board[row][col+1] == WHITE_CHAR or board[row][col+1] == CORNER_CHAR
	                        and board[row][col-1] == WHITE_CHAR or board[row][col-1] == CORNER_CHAR
	                        board[row][col] = UNOCCUPIED_CHAR
	                elif col == W2_y:
	                    if board[row+1][col] == UNOCCUPIED_CHAR or board[row+1][col] == CORNER_CHAR
	                        board[row-1][col] == UNOCCUPIED_CHAR or board[row-1][col] == CORNER_CHAR
	                        board[row][col] = UNOCCUPIED_CHAR


def createState(content):
    board = [["" for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    i=0
    j=0
    for line in content[:BOARD_SIZE]:
        for char in line:
            if char == " ":
                continue
            elif char != "\n":
                board[i][j] = char
                j+=1
            else:
                i+=1
                j=0
    return board

inFile = sys.stdin
content = inFile.readlines()
board = createState(content)
if content[BOARD_SIZE] == "Moves\n":
    print(findMoves(board, True)[1])
    print(findMoves(board, False)[1])
if content[BOARD_SIZE] == "Massacre\n":
    print(massacre(board))
