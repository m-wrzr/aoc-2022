from typing import List, Tuple

"""
First half of each round, each Elf considers the eight positions adjacent to themself
!! If no other Elves are in one of those eight positions, the Elf does not do anything during this round

otherwise:
   If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
   If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
   If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
   If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.

if two elves move to the proposed tile, no one moves
at the end of the round, the first direction the Elves considered is moved to the end of the list of directions
"""


elves = {}


class Elf:

    i: int
    j: int

    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __repr__(self) -> str:
        return f"Elf({self.i}, {self.j})"

    # If no other Elves are in one of those eight positions, the Elf does not do anything
    def next_move(self) -> Tuple[int, int]:
        """Returns the next move for this elf"""

        result = None
        free = []

        # e.g. N
        for offsets, move_to in NEXT_DIRECTION:

            free.append(True)

            # e.g. NW, NE, N
            for offset in offsets:

                free[-1] = free[-1] and (
                    (self.i + offset[0], self.j + offset[1])
                    not in elves
                    # and 0 <= (self.i + offset[0]) < N
                    # and 0 <= (self.j + offset[1]) < M
                )

            if free[-1] and not result:
                result = (self.i + move_to[0], self.j + move_to[1])

        # all neighbours are free, don't move
        if all(free):
            return None

        return result

    def positions_covered(self) -> List[Tuple[int, int]]:
        """Returns the free positions covered by this elf"""
        result = []

        for dirs, _ in NEXT_DIRECTION:
            for pos in dirs:
                if pos not in elves and 0 <= pos[0] < N and 0 <= pos[1] < M:
                    result.append((self.i + pos[0], self.j + pos[1]))

        return result


def get_min_max():
    minx, maxx, miny, maxy = 1_000_000, 0, 1_000_000, 0
    for pos in elves.keys():
        minx = min(minx, pos[0])
        maxx = max(maxx, pos[0])
        miny = min(miny, pos[1])
        maxy = max(maxy, pos[1])

    return minx, maxx, miny, maxy


# based on proposed order
NEXT_DIRECTION = [
    ([(-1, 0), (-1, -1), (-1, 1)], (-1, 0)),  # N
    ([(1, 0), (1, -1), (1, 1)], (1, 0)),  # S
    ([(0, -1), (-1, -1), (1, -1)], (0, -1)),  # W
    ([(0, 1), (-1, 1), (1, 1)], (0, 1)),  # E
]


with open("input.txt", encoding="utf-8") as f:
    lines = f.readlines()

    N, M = len(lines), len(lines[0].rstrip())

    for i, line in enumerate(lines):
        for j, c in enumerate(line.rstrip()):
            if c == "#":
                elves[(i, j)] = Elf(i, j)


CYCLE = 0


while True:

    moves = {}

    # proposal phase
    for _, elf in elves.items():
        move = elf.next_move()
        moves[move] = moves.get(move, []) + [elf]

    if len(moves) == 1:
        print(f"No moves at cycle {CYCLE + 1}")
        break

    # move phase
    for move, elves_list in moves.items():

        if move and len(elves_list) == 1:
            elf: Elf = elves_list[0]

            elves.pop((elf.i, elf.j))

            elf.i, elf.j = move
            elves[move] = elf

    covered = set()

    # count covered positions
    for _, elf in elves.items():
        covered = covered.union(elf.positions_covered())

    # for task 1)
    if CYCLE == 9:
        minx, maxx, miny, maxy = get_min_max()
        rect_size = (maxx - minx + 1) * (maxy - miny + 1)
        rect_size -= len(elves)

        print(f"Free fields in cycle {CYCLE}: {rect_size}")

    # next phase
    CYCLE += 1
    NEXT_DIRECTION = NEXT_DIRECTION[1:] + [NEXT_DIRECTION[0]]
