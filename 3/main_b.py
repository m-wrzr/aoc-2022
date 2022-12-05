# two compartments per rucksack
# points for shared items

import string


def priority(letter: str) -> int:
    return (
        (26 if letter.isupper() else 0)
        + string.ascii_lowercase.index(letter.lower())
        + 1
    )


score = 0

with open("input.txt") as f:

    lines, i = [l.rstrip("\n") for l in f.readlines()], 0

    while i < len(lines):
        a, b, c = [set(j) for j in lines[i : i + 3]]

        common = a.intersection(b).intersection(c)
        score += priority(list(common)[0])
        i += 3


print(score)
