"""Collect failed sweep points without requiring OpenFOAM."""

from pyRunOF.sweep import ParametricSweep, SweepExecutionError, SweepPoint


def calculate(point: SweepPoint) -> float:
    denominator = point.parameters["denominator"]
    return 10 / denominator


def main() -> None:
    sweep = ParametricSweep({"denominator": [2, 0, 5]})
    results = sweep.run(calculate, on_error="continue")

    for result in results:
        if isinstance(result, SweepExecutionError):
            print(f"Skipped {result.point.name}: {result.cause}")
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    main()
