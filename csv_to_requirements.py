import argparse
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        help="The sudoku as csv, underscore are missing values",
    )
    parser.add_argument("output", type=argparse.FileType("w"))
    args = parser.parse_args()

    requirements = []
    lines = args.input.read().splitlines()
    for y, line in enumerate(lines):
        for x, entry in enumerate(line.split(",")):
            if entry == "_":
                continue
            version = int(entry)
            requirements.append(f"sudoku_{x}_{y} == {version}")
    args.output.write("\n".join(requirements))


if __name__ == "__main__":
    main()
