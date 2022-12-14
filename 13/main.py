# IF both values are integers, the lower integer should come first
# IF both values are lists, compare the first value of each list, then the second value, and so on
#    in case if the right side ran out of value, false, otherwise true
# If exactly one value is an integer, convert the integer to a list which contains that integer as its only value
import ast
from functools import cmp_to_key

# ! success on first integer comparison
def compare(l: any, r: any) -> int:

    # for == case, use next result or int comparison
    if isinstance(l, int) and isinstance(r, int):
        if l == r:
            return 0

        return -1 if l < r else 1

    if isinstance(l, int) and isinstance(r, list):
        return compare([l], r)

    if isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])

    if isinstance(l, list) and isinstance(r, list):
        for (li, ri) in zip(l, r):
            x = compare(li, ri)

            if x:
                return x

        return compare(len(l), len(r))

    raise Exception("Invalid input")


with open("input.txt") as f:

    lines = [line.strip() for line in f.readlines() if line.strip()]
    lines = [lines[i : i + 2] for i in range(0, len(lines), 2)]

    result = 0

    packets = [[[2]], [[6]]]

    for i, (l, r) in enumerate(lines):

        l = ast.literal_eval(l)
        r = ast.literal_eval(r)

        packets += [l, r]

        if compare(l, r) == -1:
            result += i + 1

    print(f"result comparison: {result}")

    packets = sorted(packets, key=cmp_to_key(compare))
    print(f"result dividers: {(packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)}")
