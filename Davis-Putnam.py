# read the input file
def read_dp(path: str):
    try:
        f = open(path)
        contents = f.readlines()
        f.close()

    except Exception:
        return list(), dict(), list()

    clauses = list()  # store clauses
    atoms = dict()  # store atoms

    i = 0
    while contents[i][0] != "0":
        each_line = contents[i].strip("\n").split()
        clauses.append(each_line)
        [atoms.setdefault(abs(int(a)), None)
         for a in each_line]  # store atoms in each clause
        i += 1

    remains = contents[i + 1:]  # ignored part after 0

    return clauses, atoms, remains


# Davis-Putnam
def davis_putnam(clauses: list, atoms: dict, cur: int):

    success = True
    for c in clauses:
        base = False

        for literal in c:

            # get the value of this atom
            val = int(literal)
            if val >= 0:
                a = atoms[val]
            else:
                a = atoms[-val]
                a = None if a is None else not a

            base = base or a if a is not None else None  # check the result of this literal
            # break if missing value or fail
            if base or base is None:
                break

        # stop if fail
        if base is False:
            return False

        success &= base is True

    # find solution
    if success:
        return True

    atoms[cur + 1] = True
    if davis_putnam(clauses, atoms, cur + 1):
        return True
    else:
        atoms[cur + 1] = False
        return davis_putnam(clauses, atoms, cur + 1)


if __name__ == "__main__":
    clauses, atoms, remains = read_dp("dp_input.txt")
    atoms[1] = True
    davis_putnam(clauses, atoms, 1)
    print(atoms)
