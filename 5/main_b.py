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

        l_tmp = []

        for _ in range(repeat + 1):
            l_tmp += terminals[c_from].pop()

        l_tmp.reverse()
        terminals[c_to] += l_tmp


result = ""
for t in terminals:
    result += t[-1]

print(result)
