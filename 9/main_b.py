# head & tail of rope -> end moves if head is pulled
# must always be touching, diagoally/vertically/horizontally/overlapping

# for vertical/horizontal it stays in same lane
# for diagonal it moves to the v/h lane on 2nd move
# ? what directtion diagonal

# get number of positions the tail visited

rope = [(0, 0)] * 10

direction_mapping = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 0),
    "D": (-1, 0),
}
visited = set([rope[-1]])

# only move 1 step at a time, more isn't possible
def move_offset(offset: int):
    if offset > 0:
        return 1
    if offset < 0:
        return -1
    return 0


def pull_rope(knot: int):
    offset = (rope[knot - 1][0] - rope[knot][0], rope[knot - 1][1] - rope[knot][1])

    # don't move if knots are adjacent
    if abs(offset[0]) <= 1 and abs(offset[1]) <= 1:
        return

    rope[knot] = (
        rope[knot][0] + move_offset(offset[0]),
        rope[knot][1] + move_offset(offset[1]),
    )


with open("input.txt") as f:
    while line := f.readline().strip():
        direction, n = line.split()
        direction, n = direction_mapping[direction], int(n)

        for _ in range(n):
            rope[0] = (rope[0][0] + direction[0], rope[0][1] + direction[1])

            for k in range(1, 10):
                pull_rope(k)

            visited.add(rope[-1])

print(f"visited {len(visited)} positions")
