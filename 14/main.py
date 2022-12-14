# two-dimensional vertical slice
# x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down

# sand from src -> 500,0
# down one step if air
# down one left one, down one right one if sand/rock

# to really drop, it needs to move 1 down and rest
import numpy as np

# fill rocks for line
def draw_line(t1, t2):
    line, l_x, l_y = set(), t2[0] - t1[0], t2[1] - t1[1]

    for x in np.linspace(0, l_x, abs(l_x) + 1):
        for y in np.linspace(0, l_y, abs(l_y) + 1):
            line.add((int(t1[0] + x), int(t1[1] + y)))

    return line


filled = set()

with open("input.txt") as f:
    while line := f.readline().strip():
        coords = [tuple([int(c) for c in l.split(",")]) for l in line.split(" -> ")]

        for i in range(len(coords) - 1):
            filled.update(draw_line(coords[i], coords[i + 1]))


# can't drop lower than smallest rock
sand = (500, 0)

count = 0
floor = max([c[1] for c in filled])
below = False

# draw snd floor
filled.update(draw_line((0, floor + 2), (1000, floor + 2)))

prev = len(filled)

while True:

    d, l, r = (
        (sand[0], sand[1] + 1),
        (sand[0] - 1, sand[1] + 1),
        (sand[0] + 1, sand[1] + 1),
    )

    if d not in filled:
        sand = d
        continue

    if l not in filled:
        sand = l
        continue

    if r not in filled:
        sand = r
        continue

    # reached (500, 0)
    if sand in filled:
        break

    filled.add(sand)

    # count sand until overflow
    if sand[1] < floor and not below:
        count += 1
    else:
        below = True

    sand = (500, 0)


print(f"sand moved - fst: {count}")
print(f"sand moved - snd: {len(filled) - prev}")
