from functools import cache

# The walls of the valley are drawn as #; everything else is ground.
# Clear ground - where there is currently no blizzard - is drawn as .
# Otherwise, blizzards are drawn with an arrow indicating their
# direction of motion: up (^), down (v), left (<), or right (>)

# if they hit a wall, a new blizzard is spawned on the opposite side of the wall
# blizzards can overlap, one tile per minute

# move up, down, left, or right, or you can wait in place

# basic visited set doesn't work, because blizzard moves. step back might be needed

field, walls = dict(), set()


with open("input.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()

    N, M = len(lines), len(lines[0])

    start, end = (0, 1), (N - 1, M - 1)

    for i, line in enumerate(lines):
        for j, c in enumerate(line):

            if c == "#":
                walls.add((i, j))
                continue

            if c != ".":
                field[(i, j)] = [c]


directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "#": (0, 0),
}


@cache
def get_blizzard(step: int = 0):
    """blizzard state for the given step"""
    if step == 0:
        return field

    blizz = dict()

    for (i, j), vs in get_blizzard(step - 1).items():
        for v in vs:

            pos = (i + directions[v][0], j + directions[v][1])

            # respawn on other side
            if pos in walls:
                match v:
                    case "^":
                        blizz[(N - 2, j)] = blizz.get((N - 2, j), []) + ["^"]
                    case "v":
                        blizz[(1, j)] = blizz.get((1, j), []) + ["v"]
                    case ">":
                        blizz[(i, 1)] = blizz.get((i, 1), []) + [">"]
                    case "<":
                        blizz[(i, M - 2)] = blizz.get((i, M - 2), []) + ["<"]
            else:
                blizz[pos] = blizz.get(pos, []) + [v]

    return blizz


def find_goal(step, position_start, goal):
    """wrapper to find goal for a given start position"""

    positions = set([position_start])

    while True:

        positions_next = set()

        # iterate over possible next positions
        for (i_base, j_base) in positions:
            for (offset_i, offset_j) in directions.values():

                i, j = i_base + offset_i, j_base + offset_j

                if (i, j) == goal:
                    print(f"Found goal at step {step - 1}! (i, j): {i, j}")
                    return step - 1

                if (i, j) in walls:
                    continue

                if (i, j) in get_blizzard(step):
                    continue

                if i < 0 or i >= N or j < 0 or j >= M:
                    continue

                positions_next.add((i, j))

        positions = positions_next
        step += 1


# from start -> end -> start -> end
S = find_goal(step=0, position_start=start, goal=end)
S = find_goal(step=S, position_start=end, goal=start)
S = find_goal(step=S, position_start=start, goal=end)
