# ore collector
# clay collector
# obsidian collector
# geode-cracker
# each robot can collect 1 per minute
# construction of a robot takes 1 minute

# which blueprint is the most efficient to build? max geodes
# maximize for 24 minutes of time

# approach is probably to do some seach / state machine

import re


BLUEPRINT = []
blueprints: list[list[tuple[int, int, int, int]]] = []

with open("input.txt", encoding="utf-8") as f:
    lines = [l for l in f.read().splitlines() if l]

    def parse_line(line: int):
        """_summary_"""
        return [int(c) for c in re.findall(r"\d+", line)]

    for i, line in enumerate(lines):
        line_split = line.split(":")[1].split(".")

        blueprint = []

        ore = parse_line(line_split[0])[0]
        blueprint.append((ore, 0, 0, 0))

        ore = parse_line(line_split[1])[0]
        blueprint.append((ore, 0, 0, 0))

        ore, clay = parse_line(line_split[2])
        blueprint.append((ore, clay, 0, 0))

        ore, obsidian = parse_line(line_split[3])
        blueprint.append((ore, 0, obsidian, 0))

        blueprints.append(blueprint)

# 0: ore, 1: clay, 2: obsidian, 3: geode


def can_build(r_index: int, resources: tuple):
    """check for resources"""
    return all([BLUEPRINT[r_index][i] <= resources[i] for i in range(4)])


def build(r_index: int, robots: tuple, resources: tuple) -> tuple[tuple, tuple]:
    """subtract resources and add robot"""

    robots, resources = list(robots), list(resources)

    robots[r_index] += +1

    for j in range(4):
        resources[j] -= BLUEPRINT[r_index][j]

    return tuple(robots), tuple(resources)


def harvest(robots: tuple, resources: tuple, step: int = 0, max_step: int = 24):
    """recursive search for max geodes"""
    global GEODES

    if step == max_step:
        # print for visibility, as this runs a while
        if resources[3] > GEODES:
            GEODES = resources[3]
            print(f"FOUND NEW MAX: {GEODES}, {robots}, {resources}")
        return

    # already explored search space, don't revisit
    signature = (tuple(robots), tuple(resources), step)

    if signature in EXPLORED:
        return
    else:
        EXPLORED.add(signature)

    # check if we can reach the max with steps left and building a new geode-cracker each step
    if resources[3] + sum([(robots[3] + tl) for tl in range(max_step - step)]) < GEODES:
        return

    # collect resources for robots
    resources_after = tuple([resources[j] + robots[j] for j in range(4)])

    # prefer later robots in search space
    for j in reversed(range(4)):

        # don't build more than are needed for blueprint / min
        more_than_needed = robots[j] >= max([b[j] for b in BLUEPRINT])

        if can_build(j, resources) and not (j != 3 and more_than_needed):

            robots_new, resources_new = build(j, robots, resources_after)

            harvest(robots_new, resources_new, step + 1, max_step)

            # always build the geode-cracker
            if j == 3:
                return

        else:
            harvest(robots, resources_after, step + 1, max_step)


# BOTH OF THESE TAKE QUITE A WHILE TO RUN, UNCOMMENT TO RUN PART X

# PART 1)

QUALITY = 0

for b_id, bp in enumerate(blueprints):
    print(bp)

    BLUEPRINT, GEODES, EXPLORED = bp, 0, set()

    print(f"-------- blueprint {b_id} -------")
    harvest((1, 0, 0, 0), (0, 0, 0, 0), 0)
    print(f"-------- geodes {GEODES} -------")
    QUALITY += (b_id + 1) * GEODES
    print("---------------------------------\n\n")

print(f"Result: quality={QUALITY}")

# PART 2)

RESULT = 1

for b_id in range(3):

    # skip for sample input
    if len(blueprints) == b_id:
        continue

    BLUEPRINT, GEODES, EXPLORED = blueprints[b_id], 0, set()

    print(f"-------- blueprint {b_id} -------")
    harvest((1, 0, 0, 0), (0, 0, 0, 0), 0, max_step=32)
    print(f"-------- geodes {GEODES} -------")
    RESULT = RESULT * GEODES
    print("---------------------------------\n\n")

print(f"Result: multiplied={RESULT}")
