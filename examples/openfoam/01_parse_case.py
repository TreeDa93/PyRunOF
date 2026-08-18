"""Parse selected dictionaries from an existing OpenFOAM case."""

from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = PROJECT_ROOT / "examples" / "workflows" / "parametric_sweep" / "settings" / "base_case"


def main() -> None:
    case = OpenFOAMCase(CASE_PATH)
    settings = case.parser.parse(
        sections=("constant", "system"),
        files={
            "constant": ["transportProperties"],
            "system": ["controlDict"],
        },
    )

    print(f"Case: {settings['case']['name']}")
    print(f"Solver: {settings['system']['controlDict']['application']}")
    print(f"Viscosity: {settings['constant']['transportProperties']['nu']}")


if __name__ == "__main__":
    main()
