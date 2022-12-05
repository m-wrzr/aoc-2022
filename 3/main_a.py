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

    while line := f.readline().rstrip("\n"):
        split = int(len(line) / 2)

        a, b = line[:split], line[split:]
        a, b = set(a), set(b)

        score += priority(list(a.intersection(b))[0])

print(score)
