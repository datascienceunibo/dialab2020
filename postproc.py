#! /usr/bin/env python3


from pathlib import Path

import nbformat


PREFIX_SOL = "##sol\n"
PREFIX_NOSOL = "##nosol\n"


def load_notebook(nbfile):
    with open(nbfile, "r") as f:
        return nbformat.read(f, nbformat.NO_CONVERT)

def save_notebook(nb, nbfile):
    with open(nbfile, "w") as f:
        nbformat.write(nb, f)

def process_notebook(nb):
    nb_nosol = nbformat.v4.new_notebook()
    nb_sol = nbformat.v4.new_notebook()
    for cell in nb.cells:
        if cell.cell_type == "code" and cell.source.startswith(PREFIX_SOL):
            cell.source = cell.source.lstrip(PREFIX_SOL)
            nb_sol.cells.append(cell)
        elif cell.cell_type == "code" and cell.source.startswith(PREFIX_NOSOL):
            cell.source = cell.source.lstrip(PREFIX_NOSOL)
            nb_nosol.cells.append(cell)
        else:
            nb_nosol.cells.append(cell)
            nb_sol.cells.append(cell)
    return nb_nosol, nb_sol

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("notebook_file")
    args = parser.parse_args()
    input_path = Path(args.notebook_file)
    base_file_name = input_path.stem
    nosol_path = input_path.parent / (base_file_name + ".nosol.ipynb")
    sol_path = input_path.parent / (base_file_name + ".sol.ipynb")
    input_nb = load_notebook(input_path)
    nosol_nb, sol_nb = process_notebook(input_nb)
    save_notebook(nosol_nb, nosol_path)
    save_notebook(sol_nb, sol_path)


if __name__ == "__main__":
    main()
