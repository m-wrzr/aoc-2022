# $ -> cd (x, .., /) and ls (size name, dir name)
# determine total size of each directory
# 1)
# -> find all directories with total size at most 100k, then calculate sum
from dataclasses import dataclass
from pathlib import Path
from typing import List

recursive_sum = 0


@dataclass
class Dir:
    path: Path
    size: int


class Node:
    dir: Dir
    parent: Dir
    children: List[Dir]

    def __init__(self, dir, parent) -> None:
        self.dir = dir
        self.parent = parent
        self.children = []

    def get_size(self) -> int:
        size_overall = self.dir.size + sum([c.get_size() for c in self.children])

        # calcuate solution
        global recursive_sum
        if size_overall <= 100000:
            recursive_sum += size_overall

        print(self.dir.path, size_overall, "smaller" if size_overall <= 100000 else "")

        return size_overall


root: Node = Node(Dir(Path("/"), 0), None)
node = root


def run_cmd(line):
    global node

    # clear current path dir, avoid double count
    if line.startswith("ls"):
        node.dir.size = 0
        return

    # add directory to current path
    if line.startswith("cd"):
        args = line.split(" ")[-1]

        if args == "..":
            # TODO: might be oob
            node = node.parent
        elif args == "/":
            node = root
        else:

            # TODO: double count
            current = Node(Dir(node.dir.path / args, 0), node)
            node.children.append(current)

            node = current


with open("input.txt") as f:

    while line := f.readline().strip():

        if line.startswith("$"):
            run_cmd(line[2:])
        elif line.startswith("dir"):
            pass
        else:
            size, _ = line.split(" ")
            node.dir.size += int(size)


root.get_size()
print(recursive_sum)
