# visible if all of the other trees between it and an edge of the grid are shorter
# height map example
# 30373
# 25512
# 65332
# 33549
# 35390
# count numer of trees visible from the perspective of each tree
# -> find largest scenic score

from functools import reduce
import numpy as np

scenic_score = 0

# count elements in array until condition is met
def count_until(arr, height):
    count = 0
    for x in arr:
        count += 1

        if x >= height:
            break

    return count


with open("input.txt") as f:

    # read list of strings into two dimensional array and convert to int
    arr = [[int(x) for x in list(line.strip())] for line in f.readlines()]

    # convert this to a numpy array
    arr = np.array(arr)
    n, m = len(arr), len(arr[0])

    for i in range(1, n - 1):
        for j in range(1, m - 1):

            l, r, t, b = (
                arr[i, :j][::-1],
                arr[i, j + 1 :],
                arr[:i, j][::-1],
                arr[i + 1 :, j],
            )

            # multiple elements of array
            score = reduce(
                lambda x, y: x * y,
                [count_until(x, arr[i][j]) for x in [l, r, t, b]],
            )
            scenic_score = max(scenic_score, score)

print(scenic_score)
