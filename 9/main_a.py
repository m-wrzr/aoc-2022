# head & tail of rope -> end moves if head is pulled
# must always be touching, diagoally/vertically/horizontally/overlapping

# for vertical/horizontal it stays in same lane
# for diagonal it moves to the v/h lane on 2nd move
# ? what directtion diagonal

# get number of positions the tail visited

head, tail = (0, 0), (0, 0)

direction_mapping = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 0),
    "D": (-1, 0),
}
visited = set([tail])


def pull_rope(direction: tuple[int, int] = (0, 0)):
    global head, tail

    # no need to move tail if head is 1 away (i.e. on diagonal axis)
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return

    # move tail to head, always on off based on directionality
    tail = (head[0] - direction[0], head[1] - direction[1])

    visited.add(tail)


with open("input.txt") as f:
    while line := f.readline().strip():
        direction, n = line.split()
        direction, n = direction_mapping[direction], int(n)

        for _ in range(n):
            # move head into direction
            head = (head[0] + direction[0], head[1] + direction[1])

            pull_rope(direction)

print(f"visisted {len(visited)} positions")
