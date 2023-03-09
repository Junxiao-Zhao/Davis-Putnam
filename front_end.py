import re
from collections import defaultdict


# The player is only at one place at a time
def categ1(nodes: list, adj: defaultdict, num_steps: int):
    proposition = "~At({},%d) V ~At({},%d)\n"
    propos = list()  # store the proposition between nodes

    # format and add the pairs
    for i, n1 in enumerate(nodes):
        for n2 in nodes[i + 1:]:
            propos.append(proposition.format(n1, n2))

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps + 1):
        for p in propos:
            outputs.append(p % (i, i))

    return outputs


# read the input file
def read_front(path: str):
    nodes = list()
    treasures = list()
    num_steps = 0
    adj = defaultdict(dict)  # adjacent list of the graph

    try:
        f = open(path)
        contents = f.readlines()
        f.close()

        nodes = contents[0].split()
        treasures = contents[1].split()
        num_steps = int(contents[2].split()[0])

        for line in contents[3:]:
            c = re.split(" TREASURES| NEXT|\n", line)[:3]
            adj[c[0]]["TREASURES"] = c[1].split()
            adj[c[0]]["NEXT"] = c[2].split()

    except Exception as e:
        print(e)

    return nodes, treasures, num_steps, adj


if __name__ == "__main__":
    nodes, treasures, num_steps, adj = read_front("FrontEndInput.txt")
    print(categ1(nodes, adj, num_steps))
