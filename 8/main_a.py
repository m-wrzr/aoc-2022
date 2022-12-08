# visible if all of the other trees between it and an edge of the grid are shorter
# height map example
# 30373
# 25512
# 65332
# 33549
# 35390
# how many trees are visible from outside the grid?

import numpy as np

with open("input.txt") as f:

    # read list of strings into two dimensional array and convert to int
    arr = [[int(x) for x in list(line.strip())] for line in f.readlines()]

    # convert this to a numpy array
    arr = np.array(arr)

    n, m = len(arr), len(arr[0])

    visible = 2 * n + 2 * (m - 2)  # edges of the grid are always visible

    for i in range(1, n - 1):
        for j in range(1, m - 1):

            l, r, t, b = (
                max(arr[i, :j]),
                max(arr[i, j + 1 :]),
                max(arr[:i, j]),
                max(arr[i + 1 :, j]),
            )

            if min(l, r, t, b) < arr[i, j]:
                visible += 1

    print(visible)
