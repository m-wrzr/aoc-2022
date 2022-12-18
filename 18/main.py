# 1x1x1 cubes on a 3D grid, each given as its x,y,z position
# To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube
# example:  1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides
# each cube is 1x1x1!


lava = set()

with open("input.txt", "r") as f:
    for l in f.read().splitlines():
        lava.add(tuple([int(s) for s in l.strip().split(",")]))


# get all 6 x,y,z neighbours of a cube
def get_neighbours(x: int, y: int, z: int) -> list:
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


# check for field constraints
def is_in_bounds(x, y, z) -> bool:
    return (
        x >= minx and y >= miny and z >= minz and x <= maxx and y <= maxy and z <= maxz
    )


# count the number of sides exposed for a cube
def count_sides(cube: tuple, lava: set, water: set = set()) -> int:

    # ignore lava fields, cover always
    neighbours = [n for n in get_neighbours(*cube) if n not in lava]
    count_side = 0

    for x, y, z in neighbours:

        # extra check for part 2
        if water:
            if (x, y, z) in water or not is_in_bounds(x, y, z):
                count_side += 1
        else:
            count_side += 1

    return count_side


print(
    f"1) # sides exposed: {sum([count_sides(cube, list(lava)) for cube in sorted(lava)])}"
)


# 2) trapped air doesn't count towards the surface area


minx, maxx = min([c[0] for c in lava]) - 1, max([c[0] for c in lava]) + 1
miny, maxy = min([c[1] for c in lava]) - 1, max([c[1] for c in lava]) + 1
minz, maxz = min([c[2] for c in lava]) - 1, max([c[2] for c in lava]) + 1


water = set()
flood = [(minx, miny, minz)]

# flood fill all reachable x,y,z positions
# stop if no other positions are reachable
while flood:

    cube = flood.pop(0)

    if cube in water:
        continue

    water.add(cube)

    # ignore out of bounds
    neighbours = [
        (x, y, z) for x, y, z in get_neighbours(*cube) if is_in_bounds(x, y, z)
    ]

    # get neighbours that are not lava
    for x, y, z in neighbours:
        if (x, y, z) not in lava:
            flood.append((x, y, z))


print(
    f"2) # sides exposed: {sum([count_sides(cube, lava, water) for cube in sorted(lava)])}"
)
