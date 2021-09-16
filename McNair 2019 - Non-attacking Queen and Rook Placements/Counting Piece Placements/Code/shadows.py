import time
import math
import itertools
import allPlacements

'''
the choose function
how many ways there are to choose r objects out of n objects
ignoring order
'''


def choose(n, r):
    # just returns the choose function of the inputs
    return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))


'''
given a size of board and the known actual values
of number of placements of all proportions of queens and rooks starting at all queens
creates the list of lower bounds
'''


def lowers(size, actuals):
    # the first lower bound is always 0
    # we cannot have a lower bound for all queens with this method
    lowers = [0]

    # for every number of rooks from 1 rook to all rooks
    for x in range(1, size + 1):
        # set the sum equal to 0
        sum = 0

        # for every set of placements with more queens
        for y in range(0, x):
            # add up the number of ways to replace queens with rooks
            sum += (actuals[y] - lowers[y]) * choose(size - y, x - y)
            print(f"\n contribution to {x} from {y} rooks: " + str((actuals[y] - lowers[y]) * choose(size - y, x - y)))

        # that total sum becomes the lower bound and is then used in the next one
        lowers.append(sum)

    # return the list of lower bounds
    return lowers


# allPlacements.vars.places = []
# for place in range(0, x):
#	allPlacements.vars.places.append(place)
# allPlacements.vars.placePerms = []
# for perm in itertools.permutations(allPlacements.vars.places):
#	if not perm in allPlacements.vars.placePerms:
#		allPlacements.vars.placePerms.append(perm)

# solveAndSaveBoardsOfSizes(8, 9)

# solveAndSaveBoardsOfSizeWithRooks(6,4,False)
# solveAndSaveBoardsOfSizeWithRooks(10,9,False)
# solveAndSaveBoardsOfSizeWithRooks(11,0)
# solveAndSaveBoardsOfSizeWithRooks(11,2)

# the lists of known actual values of the number of placements
# on different sized boards with different proportions of queens and rooks
# starting from all queens moving towards all rooks
q0 = [1]
q1 = [1, 1]
q2 = [0, 0, 2]
q3 = [0, 0, 4, 6]
q4 = [2, 8, 20, 24, 24]
q5 = [10, 50, 100, 132, 168, 120]
q6 = [4, 24, 120, 432, 996, 1184, 720]
q7 = [40, 280, 992, 2504, 5288, 8780, 9668, 5040]
q8 = [92, 736, 3464, 11416, 28860, 59472, 92632, 88488, 40320]
q9 = [352, 3168, 16048, 58792, 172992, 416088, 780488, 1049940, 894964, 362880]
q10 = [724, 7240, 46984, 232264, 900864, 2710048, 6206236, 10611384, 12951636, 9944400, 3628800]

# the list of the known values
qs = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]


# for the given sizes in the range
def lowerBounds(a, b):
    for x in range(a, b):
        # print the size being worked on
        print(f"Size: {x}")

        # print the list of lower bounds
        print(f"Lower bounds: {lowers(x, qs[x])} \n")


# unique shadows
def uniqueShadows(a, b):
    for x in range(a, b):
        print("Setup...")
        firstTime = time.time()

        # testfile = open(str(x) + "x" + str(x) + " shadows.txt", 'w')

        allPlacements.vars.places = []
        for place in range(0, x):
            allPlacements.vars.places.append(place)
        allPlacements.vars.placePerms = []
        for perm in itertools.permutations(allPlacements.vars.places):
            allPlacements.vars.placePerms.append(perm)

        # for perm in allPlacements.vars.placePerms:
        #	print(perm)

        # print("\n")

        allPlacements.vars.sum = 0
        allPlacements.vars.rows = x
        allPlacements.vars.columns = x
        allPlacements.makeEmptyBoard()
        # for ros in range(0, math.floor(3*x/4) + 1):
        #	solveAndSaveBoardsOfSizeWithRooks(x, ros, False)
        print(str(math.floor(time.time() - firstTime)) + " seconds\n")
        for ros in range(0, x + 1):
            firstTime = time.time()
            allPlacements.setTempPieces(x - ros, ros)
            testfile = open(f"{x} x {x} board, {ros} rooks shadows.txt", 'w')
            testfile.write(str(x - ros) + " queens" + "\n")
            allPlacements.makePermutations()
            allPlacements.vars.currSum = 0
            for pieces in allPlacements.vars.permutations:
                # print(str(pieces) + "\n")
                allPlacements.vars.remove = []
                if not ros == 1:
                    for placements in allPlacements.vars.placePerms:
                        # print(str(placements))
                        allPlacements.makeEmptyBoard()
                        allPlacements.vars.noScrewUps = True
                        for r in range(0, x):
                            if allPlacements.vars.noScrewUps:
                                allPlacements.placePiece(pieces[r], allPlacements.vars.realBoard, r, placements[r])

                        # print("BOARD")

                        # for ro in allPlacements.vars.realBoard:
                        #	print(ro)

                        # print("\n")

                        # checkBoard(allPlacements.vars.realBoard)

                        if allPlacements.vars.noScrewUps:
                            allPlacements.vars.sum += 1
                            allPlacements.vars.currSum += 1
                            allPlacements.saveBoard(allPlacements.vars.realBoard, testfile)
                            testfile.write("\n")
                            # print(str(placements)+" GOOD")
                            allPlacements.vars.remove.append(placements)

                for places in allPlacements.vars.remove:
                    allPlacements.vars.placePerms.remove(places)

            testfile.write("\n" + "Current Total Shadow Count: " + str(allPlacements.vars.sum) + "\n")
            testfile.write(f"Unique Shadow Count for {ros} rooks: " + str(allPlacements.vars.currSum))
            # testfile.write("\n\n----------------------------------------------------------------------------------\n\n")
            print("Size: " + str(x))
            print(str(x - ros) + " queens, " + str(ros) + " rooks")
            print(f"Unique Shadow Count for {ros} rooks: " + str(allPlacements.vars.currSum))
            print("Current Total Shadow Count: " + str(allPlacements.vars.sum))
            print(str(math.floor(time.time() - firstTime)) + " seconds\n")

        # for perm in allPlacements.vars.placePerms:
        #	print(perm)
        # print("\n")
        testfile.close()
