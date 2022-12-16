from dataclasses import dataclass
import functools
import re

"""
    
valves with flow rates
30 minutes
starting at AA

1 minute to open a valve / 1 minute to follow a tunnel from one valve to another
? what is the most pressure you can release ?

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Flow is counted as minute open * flow rate

1) what is the maximum pressure you can release in 30 minutes?
2) what is the maximum pressure you can release in 26 minutes with an elephant?

"""
valves = {}


@dataclass
class Valve:
    name: str
    flow: int
    children: list


with open("input.txt") as f:
    while line := f.readline().strip():
        valve, flow_rate = re.findall(
            r"([A-Z]{2}) has flow rate=(\d+)", line.split(";")[0]
        )[0]

        valves[valve] = Valve(
            valve,
            int(flow_rate),
            re.findall(r"([A-Z]{2})", line.split(";")[1]),
        )


@functools.cache
def get_max_v(func, opened: frozenset, node: str, steps: int):
    # get best score from children
    scores = [func(opened, c, steps - 1) for c in valves[node].children]

    # open valve, revisit self
    if node not in opened and valves[node].flow > 0:
        scores.append(
            valves[node].flow * (steps - 1)
            + func(
                opened.union([node]),
                node,
                steps - 1,
            )
        )

    return max(scores)


@functools.cache
def search_valves(opened: frozenset, node: str, steps: int) -> int:
    if steps <= 0:
        return 0

    return get_max_v(search_valves, opened, node, steps)


print(f"flow 1) {search_valves(frozenset(['AA']), 'AA', 30)}")


# runs a few seconds ...
@functools.cache
def search_elephant(opened: frozenset, node: str, steps: int):
    # elephant can open valves, test if we are out of steps
    if steps <= 0:
        return search_valves(opened, "AA", 26)

    return get_max_v(search_elephant, opened, node, steps)


print(f"flow 2) {search_elephant(frozenset(['AA']), 'AA', 26)}")
