from dataclasses import dataclass
from pathlib import Path
from typing import List

# $ -> cd (x, .., /) and ls (size name, dir name)
# determine total size of each directory
# 1)
# -> find all directories with total size at most 100k, then calculate sum
# 2)
# max space 70 million
# unused needed 30 million
# delete SINGLE! directory that fits closest


sizes = []


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

        global sizes
        sizes.append(size_overall)

        return size_overall


root: Node = Node(Dir(Path("/"), 0), None)
node = root


def run_cmd(line: str):
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
            # set child/parent and new current node
            current = Node(Dir(node.dir.path / args, 0), node)
            node.children.append(current)
            node = current


with open("input.txt") as f:

    line: str
    while line := f.readline().strip():

        if line.startswith("$"):
            run_cmd(line[2:])
        elif line.startswith("dir"):
            pass
        else:
            size, _ = line.split(" ")
            # add to current node
            node.dir.size += int(size)


# also fills up sizes list
free_space = 70000000 - root.get_size()

for s in sorted(sizes):
    # smallest if additional space is over 30 mil
    if free_space + s >= 30000000:
        print(s)
        break
