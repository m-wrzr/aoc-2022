highest_elf, current_elf = 0, 0

with open("input.txt") as f:

    while line := f.readline():

        # new elf
        if line == "\n":
            highest_elf = max(highest_elf, current_elf)
            current_elf = 0
            continue

        current_elf += int(line)

print(highest_elf)
