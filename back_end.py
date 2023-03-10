import re


# read the input file
def read_back(path: str):
    true_atoms = list()
    clauses = list()

    try:
        f = open(path, mode='r', encoding="utf-8-sig")
        contents = f.readlines()
        f.close()

        # store all true cases
        i = 0
        while contents[i][0] != "0":
            each_line = contents[i].strip("\n").split()
            if each_line[1] == "T":
                true_atoms.append(i)

            i += 1

        clauses = contents[i + 1:]

    except Exception as e:
        print(e)

    return true_atoms, clauses


# write the output file
def write_back(path: str, outputs: str):
    try:
        f = open(path, "w", encoding="utf-8-sig")
        f.writelines(outputs)
        f.close()

    except Exception as e:
        print(e)


# translate the Davis Putnam output to the path
def translate_path(true_atoms: list, clauses):

    sol = list()

    # match the position
    for each in true_atoms:
        pos = re.findall(r"At\(([A-Z]+),", clauses[each])
        if len(pos):
            sol.append(pos[0])
        else:
            break

    return " ".join(sol)


def main(input_file: str, output_file: str):
    true_atoms, clauses = read_back(input_file)
    if len(true_atoms) == 0:
        write_back(output_file, "NO SOLUTION")
    else:
        write_back(output_file, translate_path(true_atoms, clauses))


if __name__ == "__main__":
    main("BackEndInput.txt", "BackEndOutput.txt")
