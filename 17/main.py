"""

rock shapes repeat     
rocks get pushed to left/right during the fall

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

> push right
< push left

chamber is 7 units wide

Each rock appears so that its left edge is two units away from the left wall 
and its bottom edge is three units above the highest rock in the room

alternate between jet and falling
rock moves until it hits a wall, floor or another rock, stops at last two

edge is three units above the highest rock in the room

"""
import numpy as np
import numpy.ma as ma

# TODO: fix part 2

rocks = [
    np.matrix(s)
    for s in [
        # "-":
        [
            [1, 1, 1, 1],
        ],
        # +
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        # L
        [
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
        ],
        # |
        [
            [1],
            [1],
            [1],
            [1],
        ],
        # #
        [
            [1, 1],
            [1, 1],
        ],
    ]
]

M = np.matrix([[0] * 7 for _ in range(3)])

rock = rocks[0]
rock_count = 0

i, j, step = 0, 0, 0


# check if matrix and rock matrix have overlap
def has_overlap(i: int, j: int):
    return 2 in np.add(
        rock,
        M[i : i + rock.shape[0], j : j + rock.shape[1]],
    )


def matrix_reset():
    global M

    # first cycle always
    if step > 0:
        # remove empty rows
        while M[0, :].sum() == 0:
            M = M[1:, :]

        # add patching between next rock and previous dropped
        M = np.concatenate((np.matrix([[0] * 7 for _ in range(3)]), M), axis=0)

    # padding for next rock
    M = np.concatenate((np.matrix([[0] * 7 for _ in range(rock.shape[0])]), M), axis=0)


def matrix_strip(m):
    while m[0, :].sum() == 0:
        m = m[1:, :]
    return m


def matrix_print(m, limit=0):
    m = m.astype(str)
    m[m == "1"] = "#"
    m[m == "0"] = " "

    for r in m if not limit else m[:limit]:
        for c in r:
            print(c, end="")
        print()


matrix_reset()


with open("input_sample.txt") as f:
    vents = [(-1 if c == "<" else 1) for c in list(f.readline().strip())]


ROCK_CACHE = set()

CYCLE_FOUND = False
CYCLE_ROCKS = 0
CYCLE_HEIGHT = 0

while rock_count <= 1_000_000_000_000:

    direction = vents[step % len(vents)]

    # right
    if direction == 1 and j + rock.shape[1] < M.shape[1]:
        j += 0 if has_overlap(i, j + 1) else 1

    # left
    elif direction == -1 and j > 0:
        j -= 0 if has_overlap(i, j - 1) else 1

    # within matrix
    if i + rock.shape[0] < M.shape[0] and not has_overlap(i + 1, j):
        i += 1
    else:

        # if this has 0's, then it will overwrite previous items
        M[i : i + rock.shape[0], j : j + rock.shape[1]] = np.add(
            rock,
            M[i : i + rock.shape[0], j : j + rock.shape[1]],
        )

        rock_count += 1
        rock, i, j = rocks[rock_count % len(rocks)], 0, 2

        if CYCLE_FOUND:
            CYCLE_ROCKS += 1

        matrix_reset()

        # TODO: not sure why this doesn't work
        # TODO: cycle is detected and filling up to the 1 trillion rock count seems reasonable
        # TODO: height is off by a factor of ~1.75

        if rock_count > 2022:
            m = matrix_strip(M[:100].copy())
            r = tuple(m.A1)

            if r in ROCK_CACHE and not CYCLE_FOUND:
                CYCLE_FOUND = True
                ROCK_CACHE = set([r])

            elif r in ROCK_CACHE and CYCLE_FOUND:

                m = matrix_strip(M[:100].copy())
                nfit = (1_000_000_000_000 - rock_count) // CYCLE_ROCKS

                rock_count += CYCLE_ROCKS * nfit
                CYCLE_HEIGHT = m.shape[0] * nfit

            elif not CYCLE_FOUND:
                ROCK_CACHE.add(r)

        if rock_count == 2022:
            print(f"1) height is: {matrix_strip(M).shape[0]}")

    step += 1


matrix_strip(M)
print(f"2) height is: {matrix_strip(M).shape[0] + CYCLE_HEIGHT}")
# 1514285714288
# 2685714283160
