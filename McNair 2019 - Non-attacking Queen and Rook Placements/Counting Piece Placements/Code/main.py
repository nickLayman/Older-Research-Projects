import math
import time
import allPlacements
import shadows
import oneQueen

board = []
size = 5

for row in range(0, size):
    board.append([])
    for col in range(0, size):
        board[row].append(0)

print(board)
