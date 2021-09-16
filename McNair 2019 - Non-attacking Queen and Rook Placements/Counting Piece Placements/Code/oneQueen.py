import math
import time


def choose(a, b):
    if b <= a and b >= 0:
        return math.factorial(a) / (math.factorial(a - b) * math.factorial(b))
    return 0


def r(i, a, b, c):
    sum = 0
    for j in range(0, a + 1):
        for k in range(0, a - j + 1):
            for m in range(0, b + 1):
                sum += (4 ** j) * choose(a, j) * (2 ** k) * choose(a - j, k) * (2 ** m) * choose(b, m) * choose(c,
                                                                                                                i - j - 2 * k - m)
    return sum


def placements(row, col, n):
    sum = 0
    for i in range(0, n):
        a = min([row - 1, col - 1, n - row, n - col])
        b = min([abs(row - col), abs(n + 1 - row - col)])
        c = n - 1 - 2 * a - 2 * b
        sum += ((-1) ** i) * math.factorial(n - 1 - i) * r(i, a, b, c)
    return sum


def allPlacements(n):
    all = []
    currRow = []
    for row in range(1, n + 1):
        for col in range(1, n + 1):
            currRow.append(placements(row, col, n))
        all.append(currRow)
        currRow = []
    return all


def totalPlacementsAll(n):
    all = allPlacements(n)
    sum = 0
    for row in all:
        for col in row:
            sum += col
    return sum


def quadrantPlacements(n):
    quadrant = []
    currRow = []
    for row in range(1, round(n / 2 + .25) + 1):
        for col in range(1, round(n / 2 - .25) + 1):
            currRow.append(placements(row, col, n))
        quadrant.append(currRow)
        currRow = []
    if n % 2 == 1:
        quadrant[-1].append(placements(round(n / 2 + .25), round(n / 2 + .25), n))
    return quadrant


def totalPlacementsQuadrant(n):
    quadrant = quadrantPlacements(n)
    sum = 0
    for row in quadrant:
        for col in row:
            sum += 4 * col
    if n % 2 == 1:
        sum -= 3 * quadrant[-1][-1]
    return sum


def eighthPlacements(n):
    eighth = []
    currRow = []
    for row in range(1, round(n / 2 + .25) + 1):
        for col in range(row, round(n / 2 + .25) + 1):
            currRow.append(placements(row, col, n))
        eighth.append(currRow)
        currRow = []
    return eighth


def totalPlacementsEighth(n):
    eighth = eighthPlacements(n)
    sum = 0
    if n % 2 == 0:
        for row in eighth:
            sum += 4 * row.pop(0)
    else:
        for row in range(0, len(eighth) - 1):
            sum += 4 * eighth[row].pop(0)
            sum += 4 * eighth[row].pop(-1)
        sum += eighth[-1].pop(0)
    for row in eighth:
        for col in row:
            sum += 8 * col
    return sum


def check(start, end):
    for n in range(start, end):
        startTime = time.time()
        print(f"Size: {n}")

        print(f"{int(totalPlacementsAll(n))} from all")
        endOfAll = time.time()

        print(f"{int(totalPlacementsQuadrant(n))} from quadrant")
        endOfQuad = time.time()

        print(f"{int(totalPlacementsEighth(n))} from eighth")
        endOfEighth = time.time()

        print(f"   {endOfAll - startTime} seconds for all")
        print(f"   {endOfQuad - endOfAll} seconds for quadrant")
        print(f"   {endOfEighth - endOfQuad} seconds for eighth")

        print("\n")
