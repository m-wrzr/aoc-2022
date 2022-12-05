import re

with open("input.txt") as f:

    lines = [l.rstrip("\n") for l in f.readlines()]
    split_at = lines.index("")
    cargo, n, instructions = (
        lines[: split_at - 1],
        int(lines[split_at - 1].strip()[-1]),
        lines[split_at + 1 :],
    )

    # build cargo lists
    cargo.reverse()

    terminals = [[] for _ in range(n)]

    # at 1, 5, 9, ...
    for line in cargo:
        for i, i_crate in enumerate(range(1, n * 4, 4)):
            if line[i_crate] != " ":
                terminals[i].append(line[i_crate])

        [line[i : i + n] for i in range(0, len(line), n)]
        # print(line)

    print(terminals)

    for instruction in instructions:
        repeat, c_from, c_to = [int(i) - 1 for i in re.findall(r"\d+", instruction)]

        for _ in range(repeat + 1):
            terminals[c_to].append(terminals[c_from].pop())


result = ""
print(terminals)
for t in terminals:
    result += t[-1]

print(result)
