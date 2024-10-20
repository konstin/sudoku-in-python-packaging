# Sudoku in python packaging

Solve sudokus not in python, but in python packages.

Solving the versions of python package from your requirements is [NP-complete](https://research.swtch.com/version-sat), in the worst case it runs exponentially slow. Sudokus are also [NP-complete](http://mountainvistasoft.com/docs/ASP.pdf), which means we can solve sudokus with python packaging.

Each cell in the sudoku grid is a package
`sudoku_{x}_{y}` (0 indexed), and the version (1-9) is the value in the field, so you can write a pyproject.toml and the installed packages are the solution.

```toml
[project]
name = "sudoku"
version = "1.0.0"
dependencies = [
    "sudoku_3_1 == 2",
    "sudoku_5_7 == 6",
    "sudoku_0_7 == 5"
    ...
]
```

## Usage

You can write the sudoku as csv:

```
5,3,_,_,7,_,_,_,_
6,_,_,1,9,5,_,_,_
_,9,8,_,_,_,_,6,_
8,_,_,_,6,_,_,_,3
4,_,_,8,_,3,_,_,1
7,_,_,_,2,_,_,_,6
_,6,_,_,_,_,2,8,_
_,_,_,4,1,9,_,_,5
_,_,_,_,8,_,_,7,9
```

Convert it to requirements:

```shell
python csv_to_requirements.py sudoku.csv requirements.in
```

```
sudoku_0_0 == 5
sudoku_1_0 == 3
[...]
sudoku_7_8 == 7
sudoku_8_8 == 9
```

Solve it with your favourite package manager, e.g:

```shell
uv pip compile --find-links packages/ --no-annotate --no-header requirements.in > requirements.txt
```

or (slow)

```shell
pip-compile --find-links packages/ --no-annotate --no-header requirements.in -o requirements.txt
```

```
sudoku-0-0==5
sudoku-0-1==6
sudoku-0-2==1
sudoku-0-3==8
sudoku-0-4==4
[...]
```

Render the solution:

```shell
python render_solution.py requirements.txt
```

```
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```

Or as a oneliner:

```console
$ python csv_to_requirements.py royle.csv - | uv pip compile --find-links packages/ --no-annotate --no-header - | python render_solution.py -
Resolved 81 packages in 126ms
5,3,4,6,7,8,9,1,2
6,7,2,1,9,5,3,4,8
1,9,8,3,4,2,5,6,7
8,5,9,7,6,1,4,2,3
4,2,6,8,5,3,7,9,1
7,1,3,9,2,4,8,5,6
9,6,1,5,3,7,2,8,4
2,8,7,4,1,9,6,3,5
3,4,5,2,8,6,1,7,9
```

## Benchmark

```
$ hyperfine --warmup 5 "uv pip compile --find-links packages/ --no-index --no-annotate --no-header requirements.in"
Benchmark 1: uv pip compile --find-links packages/ --no-index --no-annotate --no-header requirements.in
  Time (mean ± σ):      29.7 ms ±   1.6 ms    [User: 29.9 ms, System: 21.0 ms]
  Range (min … max):    27.5 ms …  35.0 ms    97 runs
```

The walltime didn't vary much between the sudokus i tried.

While dependency resolution is NP-complete and their backing algorithm is usually some form of SAT solver, in reality the problem space is much smaller: packages usually depend on a single range of another package, and that range usually increasing monotonically. You almost never run into an exponential case, most resolution in python can be done without even backtracking. The performance bottleneck is instead fetching and parsing metadata, and for python specifically building source distributions.
