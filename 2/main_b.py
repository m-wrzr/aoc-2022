"""
A for Rock, B for Paper, and C for Scissors
X for Rock, Y for Paper, and Z for Scissors
1 , 2 , 3
3 pts draw
6 pts win
X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
"""
import string


def pts(letter: str) -> int:
    return string.ascii_lowercase.index(letter.lower()) + 1


loses = {
    "A": "C",
    "C": "B",
    "B": "A",
}
beats = {v: k for k, v in loses.items()}

score = 0

with open("input.txt") as f:

    while line := f.readline():
        l, r = line.strip().split(" ")

        if r == "X":
            score += 0 + pts(loses[l])

        if r == "Y":
            score += 3 + pts(l)

        if r == "Z":
            score += 6 + pts(beats[l])


print("overall:", score)
