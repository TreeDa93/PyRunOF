"""Run several simulated cases concurrently and write a status journal."""

import time
from pathlib import Path

from pyRunOF.sweep import ParametricSweep, SweepPoint


JOURNAL_PATH = Path(__file__).resolve().parent / "output" / "parallel-journal.json"


def solve(point: SweepPoint) -> str:
    for iteration in range(1, 4):
        point.log(f"solver iteration {iteration}/3")
        time.sleep(0.2)
    return f"{point.name} solved"


def main() -> None:
    sweep = ParametricSweep({"velocity": [1, 2, 3, 4]}, mode="zip")
    results = sweep.run(
        solve,
        workers=2,
        display="all",
        journal_path=JOURNAL_PATH,
        on_error="continue",
    )
    print(*results, sep="\n")
    print(f"Journal: {JOURNAL_PATH}")


if __name__ == "__main__":
    main()
