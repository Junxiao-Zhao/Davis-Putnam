import re
from collections import defaultdict, OrderedDict


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
    treasure_node = defaultdict(
        list)  # store the nodes containing each treasure

    # format and add proposition
    for n in nodes:
        for t in adj[n]['TREASURES']:
            propos.append(proposition.format(n, t))
            treasure_node[t].append(n)

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps + 1):
        for p in propos:
            outputs.append(p % (i, i))

    return outputs, treasure_node


# If the player has treasure T at time I-1,
# then the player has T at time I
def categ4(treasures: list, num_steps: int):
    proposition = "~Has({t},%d) V Has({t},%d)\n"
    propos = list()  # store the propositions

    # format and add proposition
    for t in treasures:
        propos.append(proposition.format(t=t))

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps):
        for p in propos:
            outputs.append(p % (i, i + 1))

    return outputs


# Let M1 ... Mq be the nodes that supply treasure T.
# If the player does not have treasure T at time I-1 and has T at time I,
# then at time I they must be at one of the nodes M1 ... Mq
def categ5(treasures: list, treasure_node: defaultdict, num_steps: int):
    proposition_l = "Has({t},%d) V ~Has({t},%d)"  # left part Has
    proposition_r = " V At({},%d)"  # right part At
    propos = list()  # store the propositions

    # format and add proposition
    for t in treasures:
        propos.append(proposition_l.format(t=t))
        for n in treasure_node[t]:
            propos.append(proposition_r.format(n))
        propos[-1] += '\n'

    # duplicate and replace the position
    outputs = list()
    for i in range(num_steps):
        for j, p in enumerate(propos):
            if (j % 2 == 0):
                outputs.append(p % (i, i + 1))
            else:
                outputs.append(p % (i + 1))

    return outputs


# At time 0, the player has none of the treasures
def categ7(treasures: list):
    proposition = "~Has({},0)\n"
    propos = list()  # store the propositions

    # format and add proposition
    for t in treasures:
        propos.append(proposition.format(t))

    return propos


# At time K, the player has all the treasures
def categ8(treasures: list, num_steps: int):
    proposition = "Has({},%d)\n" % num_steps
    propos = list()  # store the propositions

    # format and add proposition
    for t in treasures:
        propos.append(proposition.format(t))

    return propos


# read the input file
def read_front(path: str):
    nodes = list()
    treasures = list()
    num_steps = 0
    adj = defaultdict(dict)  # adjacent list of the graph

    try:
        f = open(path, mode='r', encoding="utf-8-sig")
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
def write_front(path: str, outputs):
    try:
        f = open(path, "w", encoding="utf-8-sig")
        f.writelines(outputs)
        f.close()

    except Exception as e:
        print(e)


# translate clauses into Davis-Putnam input format
def translate(outputs: list):
    atoms = list()

    # break into atoms
    for o in outputs:
        atoms += re.split(" V |~|\n| ", o)

    # remove duplicates
    atoms = list(OrderedDict.fromkeys(atoms))
    atoms.remove("")

    output_str = "".join(outputs)
    translations = ""

    # replace with numbers
    for i, a in enumerate(atoms):
        output_str = output_str.replace(a, str(i + 1))
        translations += str(i + 1) + " " + a + "\n"
    output_str = output_str.replace(" V ", " ")
    output_str = output_str.replace("~", "-") + "0\n" + translations

    return output_str


def main(input_file: str, output_file: str):
    nodes, treasures, num_steps, adj = read_front(input_file)

    outputs = list()
    outputs += categ1(nodes, num_steps)
    outputs += categ2(nodes, adj, num_steps)
    output, treasure_node = categ3(nodes, adj, num_steps)
    outputs += output
    outputs += categ4(treasures, num_steps)
    outputs += categ5(treasures, treasure_node, num_steps)
    outputs.append("At(START,0)\n")  # The player is at START at time 0
    outputs += categ7(treasures)
    outputs += categ8(treasures, num_steps)

    str_out = translate(outputs)
    write_front(output_file, str_out)


if __name__ == "__main__":
    main("FrontEndInput.txt", "FrontEndOutput.txt")
