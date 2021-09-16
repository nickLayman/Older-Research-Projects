# used to create permutations of pieces
import itertools

# used to check how long the program ran for
import time

# used for making the choose function and rounding the time
import math

""" 
given a board with or without some pieces placed
and a current row to place a piece
and the set of pieces to place on the board ordered by row,
finds all possible placements of those pieces
in that order on the board
"""


def placePieces(goodBoard, row, pieces):
    # sets the piece in the given row to 'piece'
    piece = pieces[row]

    # sets the given board to 'board'
    board = goodBoard

    # manually set forbidden squares to 4 if wanted
    # board[0][1] = 4

    # moves through every column in the given row
    for column in range(0, len(goodBoard[row])):
        # sets the row, column pair to 'currSquare'
        currSquare = board[row][column]

        # if the square is free or the piece is nothing
        if currSquare == 0 or piece == 0:
            # place the piece on the square
            placePiece(piece, board, row, column)

            # if no piece is attacking another piece
            if vars.noScrewUps:
                # if the piece was just placed in the last row
                if row + 1 == len(board):
                    # you've successfully placed a piece in every row
                    # if that board is unique (only an issue when placing nothing pieces)
                    # save the board with those placements
                    if board not in vars.solved_boards:
                        addToSolvedBoards(board)

                # if the piece was not placed in the last row
                else:
                    # try to place pieces in the rest of the rows
                    placePieces(board, row + 1, pieces)

            # remove the piece just placed and move over
            removePiece(board, row, column)


"""
given a preferably solved board
add it to the array of solved boards
and increase the count.
adding it to the solved boards is done square by square
so as to get around just referencing the board
because the board will get wiped later
"""


def addToSolvedBoards(board):
    # increase the count of solved boards by 1
    vars.count += 1

    # add an empty 1x0 board to be filled in
    vars.solved_boards.append([[]])

    # go through each row of the solved board
    for eachRow in range(0, len(board)):
        # go through each column of each row
        for eachColumn in range(0, len(board[eachRow])):
            # add the row, column square to the solved boards array
            vars.solved_boards[-1][-1].append(board[eachRow][eachColumn])

        # add an empty row to be filled in next
        vars.solved_boards[-1].append([])

    # since the empty row is added after one is filled in,
    # once they're all filled in, delete the last added empty row
    del vars.solved_boards[-1][-1]


'''
given the piece to place, the board,
and the row and column to place the piece
this places that piece and adds its attacks
'''


def placePiece(ppiece, board, prow, pcolumn):
    # sets the square to the piece value
    board[prow][pcolumn] = ppiece

    # adds the attacks based on the piece value
    addRestrictions(ppiece, board, prow, pcolumn)


'''
adds the attacks of a single piece at a given position on the board
used when placing a piece
'''


def addRestrictions(ppiece, board, prow, pcolumn):
    # if the piece is a queen
    if ppiece == 2:
        # add a queen's attacks
        restrictQueen(board, prow, pcolumn)

        # check to make sure the queen isn't attacking anything
        checkQueen(board, prow, pcolumn)

    # if the piece is a rook
    if ppiece == 3:
        # add a rook's attacks
        restrictRook(board, prow, pcolumn)

        # check to make sure the rook isn't attacking anything
        checkRook(board, prow, pcolumn)


'''
given a board,
goes through every square, checks the piece, 
and adds all the attacks of those pieces.
used when removing a piece
'''


def addAllRestrictions(board):
    # goes through every row on the board
    for rrow in range(0, len(board)):
        # goes through every column in those rows
        for ccolumn in range(0, len(board[rrow])):
            # sets the current square's values to 'tile'
            tile = board[rrow][ccolumn]

            # if tile is a queen
            if tile == 2:
                # add a queen's attacks
                restrictQueen(board, rrow, ccolumn)

                # check to make sure the queen isn't attacking anything
                checkQueen(board, rrow, ccolumn)

            # if tile is a rook
            if tile == 3:
                # add a rook's attacks
                restrictRook(board, rrow, ccolumn)

                # check to make sure the rook isn't attacking anything
                checkRook(board, rrow, ccolumn)


'''
given the board and a row and column
adds a queen's attacks
and sets the position to a queen
'''


def restrictQueen(board, pRow, pColumn):
    # adds the row attacks
    restrictRow(board, pRow)

    # adds the column attacks
    restrictColumn(board, pColumn)

    # adds the diagonal attacks
    restrictDiagonals(board, pRow, pColumn)

    # sets the square to a queen
    board[pRow][pColumn] = 2


'''
given the board and a row and column
checks if a queen in that position would attack other pieces
'''


def checkQueen(board, pRow, pColumn):
    # assumes there's no screwups
    # doesn't cause issues because iff there's no issues, the next piece is placed
    vars.noScrewUps = True

    # checks if there's a piece in this row that would be attacked
    checkRow(board, pRow, pColumn)

    # checks if there's a piece in this column that would be attacked
    checkColumn(board, pRow, pColumn)

    # checks if there's a piece on the diagonals that would be attacked
    checkDiagonals(board, pRow, pColumn)


'''
given the board, a row, and a column
sets the attacks of a rook in that position
'''


def restrictRook(board, pRow, pColumn):
    # sets the attacks in the row
    restrictRow(board, pRow)

    # sets the attacks in the columns
    restrictColumn(board, pColumn)

    # sets the square to a rook
    board[pRow][pColumn] = 3


'''
given a board and a row and column,
checks if a rook in that position would attack other pieces
'''


def checkRook(board, pRow, pColumn):
    # assumes there's no screwups
    # doesn't cause issues because iff there's no issues, the next piece is placed
    vars.noScrewUps = True

    # checks if there's a piece in this row that would be attacked
    checkRow(board, pRow, pColumn)

    # checks if there's a piece in this column that would be attacked
    checkColumn(board, pRow, pColumn)

    # checks if there's a queen in any of the diagonals attacking it
    checkDiagonalsForQueens(board, pRow, pColumn)


'''
given a board and a row,
sets restrictions for the whole row iff there's no piece there
'''


def restrictRow(pboard, prow):
    # goes through every column in the given row
    for col in range(0, len(pboard[prow])):
        # if there is no piece and it's not being attacked by something else
        if pboard[prow][col] == 0:
            # set it to being attacked / restricted
            pboard[prow][col] = 1


'''
given a board and a column,
sets restrictions for the whole column iff there's no piece there
'''


def restrictColumn(pboard, pcolumn):
    # goes through every row in the given column
    for rrow in pboard:
        # if there is no piece and it's not being attacked by something else
        if rrow[pcolumn] == 0:
            # set it to being attacked / restricted
            rrow[pcolumn] = 1


'''
given a board and a row and column,
sets restrictions for the diagonals iff there's no piece there
'''


def restrictDiagonals(pboard, prow, pcolumn):
    # restricts the top left to bottom right diagonal
    restrictDescendingDiagonal(pboard, prow, pcolumn)

    # restricts the bottom left to top right diagonal
    restrictAscendingDiagonal(pboard, prow, pcolumn)


'''
given a board and a row and column
set restrictions for the descending diagonal iff there's no piece there
'''


def restrictDescendingDiagonal(pboard, prow, pcolumn):
    # move by 1
    i = 1

    # the bottom right diagonal
    # while the square you're looking at is still on the board
    while prow + i < len(pboard) and pcolumn + i < len(pboard[prow + i]):
        # if the square is free
        if pboard[prow + i][pcolumn + i] == 0:
            # set it to restricted, attacked
            pboard[prow + i][pcolumn + i] = 1

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top left diagonal
    # while the square you're looking at is still on the board
    while prow - i >= 0 and pcolumn - i >= 0:
        # if the square is free
        if pboard[prow - i][pcolumn - i] == 0:
            # set it to restricted, attacked
            pboard[prow - i][pcolumn - i] = 1

        # move one further diagonally
        i += 1


'''
given a board and a row and column
set restrictions for the ascending diagonal iff there's no piece there
'''


def restrictAscendingDiagonal(pboard, prow, pcolumn):
    # move by 1
    i = 1

    # the bottom left diagonal
    # while the square you're looking at is still on the board
    while prow + i < len(pboard) and pcolumn - i >= 0:
        # if the square is free
        if pboard[prow + i][pcolumn - i] == 0:
            # set it to restricted, attacked
            pboard[prow + i][pcolumn - i] = 1

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top right diagonal
    # while the square you're looking at is still on the board
    while prow - i >= 0 and pcolumn + i < len(pboard[prow - i]):
        # if the square is free
        if pboard[prow - i][pcolumn + i] == 0:
            # set it to restricted, attacked
            pboard[prow - i][pcolumn + i] = 1

        # move one further diagonally
        i += 1


'''
given a board, row, and column
removes any queen or rook that is there
and resets restrictions
'''


def removePiece(board, prow, pcolumn):
    # sets the current square's piece to 'thisPiece'
    thisPiece = board[prow][pcolumn]

    # if it's a queen
    if thisPiece == 2:
        # remove the queen
        deRestrictQueen(board, prow, pcolumn)

    # if it's a rook
    if thisPiece == 3:
        # remove the rook
        deRestrictRook(board, prow, pcolumn)

    # reset all the attacks
    addAllRestrictions(board)


'''
given a board, row, and column
removes a queen from the position
and removes its attacks
'''


def deRestrictQueen(board, prow, pcolumn):
    # removes the restrictions from the row
    deRestrictRow(board, prow)

    # removes the restrictions from the column
    deRestrictColumn(board, pcolumn)

    # removes the restrictions from the diagonals
    deRestrictDiagonals(board, prow, pcolumn)

    # removes the queen, sets it to a free square
    # resetting board restrictions is called after this method
    board[prow][pcolumn] = 0


'''
given a board, row, and column
removes a rook from the position
and removes its attacks
'''


def deRestrictRook(board, prow, pcolumn):
    # removes the restrictions from the row
    deRestrictRow(board, prow)

    # removes the restrictions from the column
    deRestrictColumn(board, pcolumn)

    # removes the rook, sets it to a free square
    # resetting board restrictions is called after this method
    board[prow][pcolumn] = 0


'''
given a board and row
removes restrictions from the row
does not remove pieces, just sets all restricted squares to free
'''


def deRestrictRow(pboard, rrow):
    # for each column in the given row
    for col in range(0, len(pboard[rrow])):
        # if the square is being attacked (not a piece)
        if pboard[rrow][col] == 1:
            # set the square to be free
            pboard[rrow][col] = 0


'''
given a board and column
removes restrictions from the column
does not remove pieces, just sets all restricted squares to free
'''


def deRestrictColumn(pboard, pcolumn):
    # for each row in the given column
    for rrow in pboard:
        # if the square is being attacked (not a piece)
        if rrow[pcolumn] == 1:
            # set the square to be free
            rrow[pcolumn] = 0


'''
given a board, row, and column
removes restrictions from the diagonals
does not remove pieces, just sets all restricted squares to free
'''


def deRestrictDiagonals(pboard, prow, pcolumn):
    # removes the restrictions from the descending diagonal
    # top left to bottom right
    deRestrictDescendingDiagonal(pboard, prow, pcolumn)

    # removes the restrition to the ascending diagonal
    # bottom left to top right
    deRestrictAscendingDiagonal(pboard, prow, pcolumn)


'''
given a board, row, and column
removes restrictions from the descending diagonal
does not remove pieces, just sets all restricted squares to free
'''


def deRestrictDescendingDiagonal(pboard, prow, pcolumn):
    # move by 1
    i = 1

    # the bottom right diagonal
    # while the square you're looking at is still on the board
    while prow + i < len(pboard) and pcolumn + i < len(pboard[prow + i]):
        # if the square is being attacked, not a piece
        if pboard[prow + i][pcolumn + i] == 1:
            # set it to free
            pboard[prow + i][pcolumn + i] = 0

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top left diagonal
    # while the square you're looking at is still on the board
    while prow - i >= 0 and pcolumn - i >= 0:
        # if the square is being attacked, not a piece
        if pboard[prow - i][pcolumn - i] == 1:
            # set it to free
            pboard[prow - i][pcolumn - i] = 0

        # move one further diagonally
        i += 1


'''
given a board, row, and column
removes restrictions from the ascending diagonal
does not remove pieces, just sets all restricted squares to free
'''


def deRestrictAscendingDiagonal(pboard, prow, pcolumn):
    # move by 1
    i = 1

    # the bottom left diagonal
    # while the square you're looking at is still on the board
    while prow + i < len(pboard) and pcolumn - i >= 0:
        # if the square is being attacked, not a piece
        if pboard[prow + i][pcolumn - i] == 1:
            # set it to free
            pboard[prow + i][pcolumn - i] = 0

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top right diagonal
    # while the square you're looking at is still on the board
    while prow - i >= 0 and pcolumn + i < len(pboard[prow - i]):
        # if the square is being attacked, not a piece
        if pboard[prow - i][pcolumn + i] == 1:
            # set it to free
            pboard[prow - i][pcolumn + i] = 0

        # move one further diagonally
        i += 1


'''
given a board with pieces placed
checks the entire board for mistakes
'''


def checkBoard(pboard):
    vars.noScrewUps = True
    for trow in range(0, len(pboard)):
        for tcol in range(0, len(pboard[trow])):
            if pboard[trow][tcol] == 2:
                checkRow(pboard, trow, tcol)
                checkColumn(pboard, trow, tcol)
                checkDiagonals(pboard, trow, tcol)
            if pboard[trow][tcol] == 3:
                checkRow(pboard, trow, tcol)
                checkColumn(pboard, trow, tcol)


'''
given a board, row, and column placement of a piece
checks if there's another piece in the row to attack
'''


def checkRow(bboard, pr, pc):
    # moves along the columns of a row
    for c in range(0, len(bboard[pr])):
        # checks all except the given column, which should be a piece
        if not c == pc:
            # if there's a queen or rook anywhere else in the row
            if bboard[pr][c] == 2 or bboard[pr][c] == 3:
                # something screwed up
                vars.noScrewUps = False


'''
given a board, row, and column placement of a piece
checks if there's another piece in the column to attack
'''


def checkColumn(bboard, pr, pc):
    # moves along the rows of a column
    for r in range(0, len(bboard)):
        # checks all except the given row, which should be a piece
        if not r == pr:
            # if there's a queen or rook anywhere else in the column
            if bboard[r][pc] == 2 or bboard[r][pc] == 3:
                # something screwed up
                vars.noScrewUps = False


'''
given a board, row, and column placement of a piece
checks if there's another piece in the diagonals to attack
'''


def checkDiagonals(bboard, pr, pc):
    # checks if there's a piece in the top left to bottom right diagonal
    checkDescendingDiagonal(bboard, pr, pc)
    # checks if there's a piece in the bottom left to top right diagonal
    checkAscendingDiagonal(bboard, pr, pc)


'''
given a board, row, and column placement of a piece
checks if there's another piece in the descending diagonal to attack
'''


def checkDescendingDiagonal(bboard, pr, pc):
    # move by 1
    i = 1

    # the bottom right diagonal
    # while the square you're looking at is still on the board
    while pr + i < len(bboard) and pc + i < len(bboard[pr + i]):
        # if the square has a queen or rook, it'll be being attacked
        if bboard[pr + i][pc + i] == 2 or bboard[pr + i][pc + i] == 3:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top left diagonal
    # while the square you're looking at is still on the board
    while pr - i >= 0 and pc - i >= 0:
        # if the square has a queen or rook, it'll be being attacked
        if bboard[pr - i][pc - i] == 2 or bboard[pr - i][pc - i] == 3:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1


'''
given a board, row, and column placement of a piece
checks if there's another piece in the ascending diagonal to attack
'''


def checkAscendingDiagonal(bboard, pr, pc):
    # move by 1
    i = 1

    # the bottom left diagonal
    # while the square you're looking at is still on the board
    while pr + i < len(bboard) and pc - i >= 0:
        # if the square has a queen or rook, it'll be being attacked
        if bboard[pr + i][pc - i] == 2 or bboard[pr + i][pc - i] == 3:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top right diagonal
    # while the square you're looking at is still on the board
    while pr - i >= 0 and pc + i < len(bboard[pr - i]):
        # if the square has a queen or rook, it'll be being attacked
        if bboard[pr - i][pc + i] == 2 or bboard[pr - i][pc + i] == 3:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1


def checkDiagonalsForQueens(bboard, pr, pc):
    # checks if there's a piece in the top left to bottom right diagonal
    checkDescendingDiagonalForQueens(bboard, pr, pc)
    # checks if there's a piece in the bottom left to top right diagonal
    checkAscendingDiagonalForQueens(bboard, pr, pc)


'''
given a board, row, and column placement of a piece
checks if there's another piece in the descending diagonal to attack
'''


def checkDescendingDiagonalForQueens(bboard, pr, pc):
    # move by 1
    i = 1

    # the bottom right diagonal
    # while the square you're looking at is still on the board
    while pr + i < len(bboard) and pc + i < len(bboard[pr + i]):
        # if the square has a queen, it'll be attacking the rook
        if bboard[pr + i][pc + i] == 2:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top left diagonal
    # while the square you're looking at is still on the board
    while pr - i >= 0 and pc - i >= 0:
        # if the square has a queen, it'll be attacking the rooks
        if bboard[pr - i][pc - i] == 2:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1


'''
given a board, row, and column placement of a piece
checks if there's another piece in the ascending diagonal to attack
'''


def checkAscendingDiagonalForQueens(bboard, pr, pc):
    # move by 1
    i = 1

    # the bottom left diagonal
    # while the square you're looking at is still on the board
    while pr + i < len(bboard) and pc - i >= 0:
        # if the square has a queen, it'll be attacking the rook
        if bboard[pr + i][pc - i] == 2:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1

    # move by 1
    i = 1

    # the top right diagonal
    # while the square you're looking at is still on the board
    while pr - i >= 0 and pc + i < len(bboard[pr - i]):
        # if the square has a queen, it'll be attacking the rook
        if bboard[pr - i][pc + i] == 2:
            # so something has screwed up
            vars.noScrewUps = False

        # move one further diagonally
        i += 1


# the variables necessary throughout the program
# all initialized to 0 to be changed in methods before trying to count
class vars:
    # the number of rows in the board
    rows = 0

    # the number of columns in the board
    columns = 0

    # the time the the program started
    firstTime = 0

    # the actual board
    realBoard = []

    # the permutation of pieces currently being used
    tempPieces = []

    # the list of all permutations of the pieces
    permutations = []

    # 0 - free
    # 1 - restricted
    # 2 - queen
    # 3 - rook
    # 4 - forbidden

    # the number of solved boards found
    count = 0

    # the total number of solved boards found, count is reset every permutation
    totalCount = 0

    # the actual boards that were counted as solved, in case of wanting to save them
    solved_boards = []

    # no pieces are attacking each other
    noScrewUps = True


'''
takes the initially empty 'realBoard'
adds the correct number of empty rows and columns
'''


def makeEmptyBoard():
    # resets realBoard to an empty array
    vars.realBoard = []

    # for the correct number of rows
    for row in range(0, vars.rows):
        # add an empty row
        vars.realBoard.append([])

        # for the correct number of columns
        for column in range(0, vars.columns):
            # add an empty column to this row
            vars.realBoard[row].append(0)


'''
finds all permutations of the temporary pieces
adds them to the array of permuations
'''


def makePermutations():
    # resets the array of permutations
    vars.permutations = []

    # for each permutation produced by the permutation method
    for permutation in itertools.permutations(vars.tempPieces):
        # if it is not already in the list
        # the permutation method works by position not content so this check is vital
        if permutation not in vars.permutations:
            # add it to the list
            vars.permutations.append(permutation)


'''
given a number of queens and rooks
sets the array tempPieces 
'''


def setTempPieces(numQueens, numRooks):
    # resets the array of tempPieces
    vars.tempPieces = []

    # for as many queens as is given
    for quens in range(0, numQueens):
        # add a queen
        vars.tempPieces.append(2)

    # for as many rooks as is given
    for roks in range(0, numRooks):
        # add a rook
        vars.tempPieces.append(3)


'''
given an array of pieces and a file name
saves those pieces to the file 
along with the number of placements found with those pieces
'''


def savePieces(pieces, file):
    # sets the 'current pieces' to an empty array
    cPieces = []

    # enhances readability of the saved files
    # for each piece in the given pieces
    for i in range(0, len(pieces)):
        # if its a 2
        if pieces[i] == 2:
            # that indicates a queen so add a Q
            cPieces.append("Q")

        # if its a 3
        elif pieces[i] == 3:
            # that indicates a rook so add an R
            cPieces.append("R")

        # if its anything else
        else:
            # just add whatever number it is
            cPieces.append(str(pieces[i]))

    # saves the list of pieces to the given text file
    file.write("Pieces: " + str(cPieces) + "\n")

    # saves the number of placements made with those pieces to the given text file
    file.write("Nonattacking placements: " + str(vars.count) + "\n\n")


'''
given a board and a file name
saves the board to the file
'''


def saveBoard(board, file):
    # just saving the board writes the memory location
    # for each row in the board
    for row in board:
        # for each piece in that row
        for p in row:
            # if its a queen
            if p == 2:
                # print Q
                file.write("Q ")

            # if its a rook
            elif p == 3:
                # print R
                file.write("R ")

            # if its anything else
            else:
                # print that number
                file.write(str(p) + " ")

        # each row gets put on a new line
        file.write("\n")


'''
given an array of pieces and a file name
saves the pieces and the solved boards using those pieces to the file
'''


def saveBoards(pieces, file):
    # save the list of pieces and how many boards were solved with them
    savePieces(pieces, file)

    # for each board in the list of solved boards
    for board in vars.solved_boards:
        # save the board to the file
        saveBoard(board, file)

        # add a blank line between boards
        file.write("\n")


'''
given a permutation of pieces
find all solutions of boards using that permutation
and save all those boards
'''


def solveAndCountBoardsWithPerm(permutation):
    # reset the count of solved boards
    vars.count = 0

    # reset the list of solved boards
    vars.solved_boards = []

    # nothing has gone wrong yet
    noScrewUps = True

    # find all ways to place the pieces
    placePieces(vars.realBoard, 0, permutation)

    # add this permutation's count to the total count of solved boards
    vars.totalCount += vars.count


'''
given what size we're working with and how many rooks there are
prints a small summary of the data about it
'''


def printSummary(size, numRooks=None):
    # prints out what size board we have
    print(str(vars.rows) + " x " + str(vars.columns) + " board")

    # if numRooks if given
    try:
        # print how many queens there are
        print(str(size - numRooks) + " queens")

        # print how many rooks there are
        print(str(numRooks) + " rooks")

    # if numRooks was not given
    except:
        # just print what pieces were used
        print("Pieces: " + str(vars.tempPieces))

    # print how many nonattacking placements there are with those pieces
    print("Total nonattacking placements: " + str(vars.totalCount))

    # print how long it took to find them all
    print(str(math.floor(time.time() - vars.firstTime)) + " seconds")

    # add a blank line between summaries
    print()


'''
given a size, a number of rooks, and whether to save the boards
finds all placements of a square board with queens and rooks
'''


def solveAndSaveBoardsOfSizeWithRooks(size, rooks, save=True):
    # sets the start time of this calculation
    vars.firstTime = time.time()

    # sets the number of rows to the given size
    vars.rows = size

    # sets the number of columns to the given size
    vars.columns = size

    # creates an empty board of that size
    makeEmptyBoard()

    # creates a set of pieces of queens and rooks
    setTempPieces(size - rooks, rooks)

    # creates an array of all the permuations of those pieces
    makePermutations()

    # creates a file to save everything to based on the size
    file = open(str(size) + " x " + str(size) + " board, " + str(rooks) + " rooks.txt", "w")

    # resets the total count of solved board
    vars.totalCount = 0

    # for every permutation of pieces
    for permutation in vars.permutations:
        # find all the placements with that permuation
        solveAndCountBoardsWithPerm(permutation)

        # if we were told to save the boards
        if save:
            # save the boards to the file
            saveBoards(permutation, file)

    removeSolvedBoardsFromPlacePerms(vars.solved_boards)

    # save how many total placements were found for this size with that many rooks
    file.write("Total nonattacking placements: " + str(vars.totalCount) + "\n")

    # print out a small summary of the results
    printSummary(size, rooks)

    # close the file
    file.close()


def removeSolvedBoardsFromPlacePerms(boards):
    for board in boards:
        curperm = []
        for row in board:
            try:
                curperm.append(row.index(2))
            except:
                curperm.append(row.index(3))
        try:
            vars.placePerms.remove(curperm)
        except:
            pass


'''
given a size, a list of pieces, and whether to save the boards
find all placements of a square board with those pieces
'''


def solveAndSaveBoardsOfSizeWithPieces(size, pieces, save=True):
    # sets the start time of this calculation
    vars.firstTime = time.time()

    # sets the number of rows to the given size
    vars.rows = size

    # sets the number of columns to the given size
    vars.columns = size

    # creates an empty board of that size
    makeEmptyBoard()

    # sets the set of pieces to the given pieces
    vars.tempPieces = pieces

    # creates an array of all the permuations of those pieces
    makePermutations()

    # creates a file to save everything to based on the size
    file = open(str(size) + " x " + str(size) + " board, " + str(pieces) + ".txt", "w")

    # resets the total count of solved board
    vars.totalCount = 0
    for permutation in vars.permutations:
        # find all the placements with that permuation
        solveAndCountBoardsWithPerm(permutation)

        # if we were told to save the boards
        if save:
            # save the boards to the file
            saveBoards(permutation, file)

    # save how many total placements were found for this size with that many rooks
    file.write("Total nonattacking placements: " + str(vars.totalCount) + "\n")

    # print out a small summary of the results
    # printSummary(size, rooks)

    # close the file
    file.close()


'''
given a size of board
find and save all queen/rook placements of that size
'''


def solveAndSaveBoardsOfSize(size):
    # for every proportion of queens and rooks
    for rooks in range(0, size + 1):
        # solve and save the boards of the given size with that many rooks
        solveAndSaveBoardsOfSizeWithRooks(size, rooks)


'''
given a small and large size of board
find and save all queen/rook placements of all the sizes in between
'''


def solveAndSaveBoardsOfSizes(start, end):
    # for every size from start to end (not including end)
    for s in range(start, end):
        # solve and save all the boards of that size
        solveAndSaveBoardsOfSize(s)
