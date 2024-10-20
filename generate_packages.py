from zipfile import ZipFile
from pathlib import Path

square_size = 3
grid_size = square_size**2

package_dir = Path("packages")

wheel_file_contents = """
Wheel-Version: 1.0
Generator: sudoku (1.0.0)
Root-Is-Purelib: true
Tag: py3-none-any
""".strip()


def generate_package(x: int, y: int, version: int):
    name = f"sudoku_{x}_{y}"
    dependencies = []
    # Column exclusion
    for y_ in range(grid_size):
        if y_ == y:
            continue
        dependencies.append(f"sudoku_{x}_{y_} != {version}")
    # Row exclusion
    for x_ in range(grid_size):
        if x_ == x:
            continue
        dependencies.append(f"sudoku_{x_}_{y} != {version}")
    # Square exclusion
    square_base_x = x - (x % square_size)
    square_base_y = y - (y % square_size)
    for x_ in range(square_size):
        for y_ in range(square_size):
            if square_base_x + x_ == x and square_base_y + y_ == y:
                continue
            dependencies.append(
                f"sudoku_{square_base_x+x_}_{square_base_y+y_} != {version}"
            )

    # Write the wheel
    filename = f"{name}-{version}-py3-none-any.whl"
    with ZipFile(package_dir.joinpath(filename), "w") as writer:
        metadata = [f"Name: {name}", f"Version: {version}", "Metadata-Version: 2.2"]
        for requires_dist in dependencies:
            metadata.append(f"Requires-Dist: {requires_dist}")
        writer.writestr(f"{name}-{version}.dist-info/METADATA", "\n".join(metadata))
        writer.writestr(f"{name}-{version}.dist-info/WHEEL", wheel_file_contents)
        # Not checked anyway
        record = f"{name}-{version}.dist-info/METADATA,,"
        record += f"{name}-{version}.dist-info/WHEEL,,"
        record += f"{name}-{version}.dist-info/RECORD,,"
        writer.writestr(f"{name}-{version}.dist-info/RECORD", "")


def main():
    package_dir.mkdir(exist_ok=True, parents=True)
    for x in range(grid_size):
        for y in range(grid_size):
            for version in range(1, grid_size + 1):
                generate_package(x, y, version)


if __name__ == "__main__":
    main()
