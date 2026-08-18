"""Run a Cartesian product of parameters without requiring OpenFOAM."""

from pyRunOF.sweep import ParametricSweep, SweepPoint


def calculate(point: SweepPoint) -> str:
    velocity = point.parameters["velocity"]
    model = point.parameters["model"]
    result = f"{point.name}: velocity={velocity}, model={model}"
    print(result)
    return result


def main() -> None:
    sweep = ParametricSweep(
        {
            "velocity": [1, 2],
            "model": ["kEpsilon", "kOmegaSST"],
        },
        mode="product",
    )
    results = sweep.run(calculate)
    print(f"Completed {len(results)} of {sweep.total} points")


if __name__ == "__main__":
    main()
