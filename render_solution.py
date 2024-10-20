import argparse
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "solution",
        type=argparse.FileType("r"),
        help="requirements.txt without annotations with the solution",
    )
    args = parser.parse_args()

    lines = args.solution.read().splitlines()
    grid_size = max(int(line.split("==")[1]) for line in lines)
    grid: list[list[int | str]] = [
        ["_" for _ in range(grid_size)] for _ in range(grid_size)
    ]
    for line in lines:
        package, version = line.split("==")
        _, x, y = package.split("-")
        grid[int(y)][int(x)] = int(version)
    for row in grid:
        print(",".join((str(version) for version in row)))


if __name__ == "__main__":
    main()
