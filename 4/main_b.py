score = 0

with open("input.txt") as f:

    while line := f.readline().rstrip("\n"):
        (l_low, l_up), (r_low, r_up) = [
            [int(i) for i in l.split("-")] for l in line.split(",")
        ]

        if l_low <= r_low <= l_up or l_low <= r_up <= l_up:
            score += 1
        elif r_low <= l_low <= r_up or r_low <= l_up <= r_up:
            score += 1
        else:
            pass

print(score)
