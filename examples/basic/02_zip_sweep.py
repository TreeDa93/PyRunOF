"""Combine corresponding parameter values without requiring OpenFOAM."""

from pyRunOF.sweep import ParametricSweep


def main() -> None:
    sweep = ParametricSweep(
        {
            "velocity": [1, 2, 5],
            "viscosity": [1e-6, 2e-6, 5e-6],
        },
        mode="zip",
    )

    for point in sweep:
        print(point.index, point.parameters, point.name)


if __name__ == "__main__":
    main()
