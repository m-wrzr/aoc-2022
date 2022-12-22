import re

# input is a set of open tiles, on which you can moves
# '.' is an open tile
# '#' is a wall
# moves: e.g. 10R5L5R10L4R5L5
# 10 = 10 steps forward
# R = turn right (90 degrees clockwise) / L = turn left (90 degrees counter-clockwise)
# start at: leftmost open tile of the top row of tiles. Initially, you are facing to the right
# wrap around movement: if you move off the edge of the map, you will appear on the opposite edge
# caveat: wrapped tile can be a wall, too

# answer: row, column, facing direction

with open("input.txt", encoding="utf-8") as f:
    lines = [l.rstrip() for l in f.readlines()]
    tiles, movements = [list(l) for l in lines[:-2]], re.split("(R|L)", lines[-1])

    N, M = len(tiles), max([len(tile) for tile in tiles])

    posij = (0, tiles[0].index("."))

    # make proper N * M grid
    grid = [[-1] * M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            grid[i][j] = tiles[i][j] if j < len(tiles[i]) else ""

# clockwise directions
directions, d = [(0, 1), (1, 0), (0, -1), (-1, 0)], 0

while movements:
    move = movements.pop(0)

    match move:
        case "R":
            d = (d + 1) % 4
        case "L":
            d = (d - 1) % 4
        case _:
            move = int(move)

            # store last valid position in case we wrap into a wall
            last_valid = posij

            while move > 0:

                pi = (posij[0] + directions[d][0]) % N
                pj = (posij[1] + directions[d][1]) % M

                match grid[pi][pj]:
                    case "#":
                        break
                    # walkable tile
                    case ".":
                        posij = (pi, pj)
                        last_valid = posij
                        move -= 1
                    # empty tile, increment but don't count as a valid move
                    case _:
                        posij = (pi, pj)

            posij = last_valid

print(f"Password: {1000* (posij[0] + 1) + 4*(posij[1] + 1) + d}")
