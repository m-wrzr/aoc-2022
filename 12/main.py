import string
import networkx as nx

# elevations given from a-z in a grid
# S is current position
# E is the best position

# reach E from S
# elevation can be at most 1 higher, lower is always possible


G, target, sources = nx.DiGraph(), None, []

# assign height based on letter in alphabet
def height(lines, i, j):
    global target, sources

    letter = lines[i][j]

    if letter == "a":
        sources.append((i, j))

    if letter == "S":
        sources.insert(0, (i, j))
        letter = "a"

    if letter == "E":
        letter, target = "z", (i, j)

    return string.ascii_lowercase.index(letter)


# add edges if height difference is <= 1
def add_if_valid(node, node_adj):
    if node_adj[1]["height"] <= node[1]["height"] + 1:
        G.add_edge(node[0], node_adj[0])


# helper function to construct adjecent nodes/edges
def get_node(i, j):
    return [node for node in G.nodes(data=True) if node[0] == (i, j)][0]


with open("input.txt") as f:
    lines = f.readlines()
    n, m = len(lines), len(lines[0].strip())


# build nodes
for i in range(n):
    for j in range(m):

        letter = lines[i][j]

        # map to start/end nodes
        match letter:
            case "a":
                sources.append((i, j))
            case "S":
                sources.insert(0, (i, j))
                letter = "a"
            case "E":
                target = (i, j)
                letter = "z"

        G.add_node((i, j), height=string.ascii_lowercase.index(letter))


# build edges
for i in range(n):
    for j in range(m):

        node = get_node(i, j)

        if i - 1 >= 0:
            add_if_valid(node, get_node(i - 1, j))

        if i + 1 < n:
            add_if_valid(node, get_node(i + 1, j))

        if j - 1 >= 0:
            add_if_valid(node, get_node(i, j - 1))

        if j + 1 < m:
            add_if_valid(node, get_node(i, j + 1))


paths = nx.shortest_path(G, target=target)
valid = [len(paths[source]) - 1 for source in sources if source in paths]

print(
    f"""
shortest path lenghts:
-> from {sources[0]}: {valid[0]}
-> sources "a": {min(valid)}
"""
)
