import re
from collections import defaultdict


# The player is only at one place at a time
def categ1(nodes: list, num_steps: int):
    proposition = "~At({},%d) V ~At({},%d)\n"
    propos = list()  # store the propositions

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


# The player must move on edges
def categ2(nodes: list, adj: defaultdict, num_steps: int):
    proposition_l = "~At({},%d)"  # left part at position i
    proposition_r = " V At({},%d)"  # right part at position i+1
    propos = list()  # store the propositions

    # format and add proposition
    for n1 in nodes:
        propos.append(proposition_l.format(n1))
        for n2 in adj[n1]['NEXT']:
            propos.append(proposition_r.format(n2))
        propos[-1] += "\n"

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps):
        for p in propos:
            val = i if p[0] == "~" else i + 1  # left at i, right at i+1
            outputs.append(p % val)

    return outputs


# Suppose that treasure T is located at node N.
# Then if the player is at N at time I,
# then at time I the player has T
def categ3(nodes: list, adj: defaultdict, num_steps: int):
    proposition = "~At({},%d) V Has({},%d)\n"
    propos = list()  # store the propositions

    # format and add proposition
    for n in nodes:
        for t in adj[n]['TREASURES']:
            propos.append(proposition.format(n, t))

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps + 1):
        for p in propos:
            outputs.append(p % (i, i))

    return outputs


# If the player has treasure T at time I-1,
# then the player has T at time I
def categ4(treasures: list, num_steps: int):
    proposition = "~Has({t},%d) V Has({t},%d)\n"
    propos = list()  # store the propositions

    # format and add proposition
    for t in treasures:
        propos.append(proposition.format(t=t))

    # # duplicate and replace the position
    outputs = list()
    for i in range(num_steps):
        for p in propos:
            outputs.append(p % (i, i + 1))

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


# write the output file
def write_front(path: str, outputs: list):
    try:
        f = open(path, "w", encoding="utf-8-sig")
        f.writelines(outputs)
        f.close()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    outputs = list()
    nodes, treasures, num_steps, adj = read_front("FrontEndInput.txt")

    outputs += categ1(nodes, num_steps)
    outputs += categ2(nodes, adj, num_steps)
    outputs += categ3(nodes, adj, num_steps)
    outputs += categ4(treasures, num_steps)

    write_front("FrontEndOutput.txt", outputs)
