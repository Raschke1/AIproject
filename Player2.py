from MiniMax import MiniMax
from GameTree import GameNode
from GameTree import GameTree
import copy

BOARD_SIZE = 8
BLACK_P = "B"
WHITE_P = "W"
CORNER_P = "X"
EMPTY_P = "-"

class Player:
    def __init__(self, colour):
        return

    def action(self, turn):
        action1 = int(input("Enter Move X:"))
        action2 = int(input("Enter Move Y:"))
        isMove = input("Move?:")
        if isMove == "T":
            action3 = int(input("Enter Move X:"))
            action4 = int(input("Enter Move Y:"))
            return ((action1, action2), (action3, action4))
        else:
            return (action1, action2)

    def update(self, action):
        return
