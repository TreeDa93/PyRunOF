"""Parse one file from a selected section of an existing OpenFOAM case."""

from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase


EXAMPLES_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = EXAMPLES_ROOT / "workflows" / "poiseuille_flow" / "PoiseuilleFlow"


def main() -> None:
    case = OpenFOAMCase(CASE_PATH)
    settings = case.parser.parse(
        #sections="initial_conditions",
        files={"initial_conditions": ["U"]},
    )
    inlet = settings["initial_conditions"]["U"]["boundaryField"]["inlet"]

    print(f"Case: {settings['case']['name']}")
    print(f"Inlet velocity: {inlet['value']}")


if __name__ == "__main__":
    main()
