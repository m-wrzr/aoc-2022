# sensors and beacons with x,y coordinates
# manhattan distance between them, one sensor can only be connected to one beacon
import re
import sys
import numpy as np

sensors = []
covered = set()

# TODO: both algorithms are very slow, need to optimize

distance = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])

minx, maxx = 10000000, -10000000
y_fixed, n = 2000000, 0

with open("input.txt") as f:
    while line := f.readline().strip():
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        sx, sy, bx, by = list(map(int, re.findall(r"[+-]?\d+", line)))

        dist = distance((sx, sy), (bx, by))

        minx = min(minx, sx - dist)
        maxx = max(maxx, sx + dist)

        covered.add((bx, by))
        covered.add((sx, sy))
        sensors.append((sx, sy, dist))


# 1)
for x in range(minx, maxx + 1):
    position = (x, y_fixed)

    if position in covered:
        continue

    for sx, sy, dist in sensors:

        # position already covered by another sensor
        if dist >= distance(position, (sx, sy)):
            n += 1
            break

print(f"1) y_fixed: {y_fixed} has {n} covered fields")

# 2)
# tuning frequency, which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.
is_free = lambda x, y: all([distance((x, y), (sx, sy)) > d for (sx, sy, d) in sensors])

# key insight is that the distance of a free field is always 1 more than the distance of a sensor field
for sx, sy, dist in sensors:

    # diamond shaped points around (sx,sy) with distance d+1
    pu = (sx, sy - (dist + 1))
    pl = (sx - (dist + 1), sy)
    pd = (sx, sy + (dist + 1))
    pr = (sx + (dist + 1), sy)

    positions = np.concatenate(
        (
            np.linspace(pu, pr, dist + 2),
            np.linspace(pr, pd, dist + 2),
            np.linspace(pd, pl, dist + 2),
            np.linspace(pl, pu, dist + 2),
        )
    )

    for x, y in positions:
        x = int(x)
        y = int(y)

        if (
            0 <= x <= 4000000
            and 0 <= y <= 4000000
            and distance((x, y), (sx, sy)) == dist + 1
            and is_free(x, y)
        ):
            print(f"2) distress signal is: {x * 4000000 + y}")
            sys.exit(0)
