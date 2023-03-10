# read the input file
def read_dp(path: str):

    clauses = list()  # store clauses
    atoms = dict()  # store atoms
    remains = list()

    try:
        f = open(path, mode='r', encoding="utf-8-sig")
        contents = f.readlines()
        f.close()

        i = 0
        while contents[i][0] != "0":
            each_line = contents[i].strip("\n").split()
            clauses.append(each_line)
            [atoms.setdefault(abs(int(a)), None)
             for a in each_line]  # store atoms in each clause
            i += 1

        remains = contents[i:]  # ignored part
        clauses.sort(key=lambda x: len(x))  # sort by length

    except Exception as e:
        print(e)

    return clauses, atoms, remains


# write the output file
def write_dp(path: str, atoms: dict, remains: list, success: bool):
    try:
        f = open(path, "w", encoding="utf-8-sig")

        # write solution if exits
        if success:
            f.writelines([
                " ".join([str(k), str(atoms[k])[0], "\n"])
                for k in atoms.keys()
            ])
        # write the remains
        f.writelines(remains)

        f.close()

    except Exception as e:
        print(e)


# Davis-Putnam
def davis_putnam(clauses: list, atoms: dict):

    i = 0
    while i < len(clauses):
        next_pos = True

        for j in range(len(clauses[i])):
            # get the value of this atom
            val = int(clauses[i][j])
            if val >= 0:
                a = atoms[val]
            else:
                a = atoms[-val]
                a = None if a is None else not a

            # remove the False literal
            if a is False:
                clauses[i].pop(j)
                break
            # remove the True clause
            elif a:
                clauses.pop(i)
                next_pos = False
                break

        # pure literal then failed
        if next_pos and len(clauses[i]) == 0:
            return False

        if next_pos:
            i += 1

    # empty clauses then True
    if len(clauses) == 0:
        return True
    else:
        # set an atom to True
        clauses.sort(key=lambda x: len(x))
        val = int(clauses[0][0])
        atoms[abs(val)] = True if val >= 0 else False

        # success
        if davis_putnam([c.copy() for c in clauses], atoms):
            return True
        # fail, try set to False
        else:
            atoms[abs(val)] = not atoms[abs(val)]

            # success
            if davis_putnam([c.copy() for c in clauses], atoms):
                return True
            # fail, back to previous state
            else:
                atoms[abs(val)] = None
                return False


def main(input_file: str, output_file: str):
    clauses, atoms, remains = read_dp(input_file)  # read
    sol = davis_putnam([c.copy() for c in clauses], atoms)  # solve
    write_dp(output_file, atoms, remains, sol)  # write


if __name__ == "__main__":
    main("dp_input.txt", "dp_output.txt")
