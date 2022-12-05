elves = [0]

with open("input.txt") as f:

    while line := f.readline():

        # new elf
        if line == "\n":
            elves.append(0)
            continue

        elves[-1] += int(line)

elves.sort(reverse=True)
result = sum(elves[:3])

print(result)
