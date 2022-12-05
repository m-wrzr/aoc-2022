# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors
# 1 , 2 , 3
# 3 pts draw
# 6 pts win

map_replace = {"X": "A", "Y": "B", "Z": "C"}
map_points = {"A": 1, "B": 2, "C": 3}

matchups = {
    "AB": 0,
    "BA": 6,
    "AC": 6,
    "CA": 0,
    "BC": 0,
    "CB": 6,
}


score = 0

with open("input.txt") as f:

    while line := f.readline():
        l, r = line.strip().split(" ")

        r = map_replace[r]

        score += map_points[r]

        if l == r:
            score += 3
        else:
            score += matchups[r + l]

print(score)
