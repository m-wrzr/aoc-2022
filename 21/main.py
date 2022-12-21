# either to yell a specific number or to yell the result of a math operation
# all number yelling monkeys know their number from the start
# monkeys might need to wait for numbers to be yelled

# work out the number the monkey named root will yell
# seems like we need to build a tree

from typing import Dict, Tuple

from sympy import Eq, Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers import solve

numbers: Dict[str, int] = {}
symbols: Dict[str, Tuple[str, str, str]] = {}


PART = 2


with open("input.txt", encoding="utf-8") as f:

    while line := f.readline().strip():
        node_id, operation = [l.strip() for l in line.split(":")]

        # example -> dbpl: 5
        if " " not in operation:
            numbers[node_id] = int(operation)
            if node_id == "humn" and PART == 2:
                numbers[node_id] = "X"
        # example -> dbpl: ljgn * ptdq
        else:
            ops = list(operation.split(" "))
            if node_id == "root" and PART == 2:
                ops[1] = "=="
            symbols[node_id] = tuple(ops)


def build(node: str) -> int:
    """recursively solve the tree"""
    if node in numbers:
        return numbers[node]

    l, op, r = symbols[node]

    return f"({build(l)}{op}{build(r)})"


if PART == 1:
    # build simple equation
    result = parse_expr(build("root"), evaluate=True)

if PART == 2:
    # build two-sided equation
    result = solve(
        Eq(
            parse_expr(build(symbols["root"][0]), evaluate=False),
            parse_expr(build(symbols["root"][2]), evaluate=False),
        ),
    )

print(result)
