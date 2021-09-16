import itertools
import math


def queensAbs(q):
    n = q
    perms = list(itertools.permutations(range(1, n + 1)))
    remove = []

    for x in range(math.factorial(n)):
        for i in range(n - 1):
            for j in range(i + 1, n):
                if not perms[x] in remove:
                    if abs(perms[x][i] - perms[x][j]) == abs(i - j):
                        remove.append(perms[x])

    for r in remove:
        perms.remove(r)

    showPlacements(n, perms)


def queensNoMajor(q):
    n = q
    perms = list(itertools.permutations(range(1, n + 1)))
    remove = []

    for x in range(math.factorial(n)):
        for i in range(n - 1):
            for j in range(i + 1, n):
                if not perms[x] in remove:
                    if perms[x][j] - perms[x][i] == j - i:
                        remove.append(perms[x])

    for r in remove:
        perms.remove(r)

    showPlacements(n, perms)


def queensNoMinor(q):
    n = q
    perms = list(itertools.permutations(range(1, n + 1)))
    remove = []

    for x in range(math.factorial(n)):
        for i in range(n - 1):
            for j in range(i + 1, n):
                if not perms[x] in remove:
                    if perms[x][i] - perms[x][j] == j - i:
                        remove.append(perms[x])

    for r in remove:
        perms.remove(r)

    showPlacements(n, perms)


def showPlacements(n, perms):
    print()
    zeros = []

    for x in range(n):
        zeros.append(0)

    for perm in perms:
        print(f"permutation: {perm}\nboard:")
        for c in perm:
            row = zeros
            row[c - 1] = 1
            print(f"{row}")
            row[c - 1] = 0
        print("\n")

    print(f"number of permutations: {len(perms)}")
