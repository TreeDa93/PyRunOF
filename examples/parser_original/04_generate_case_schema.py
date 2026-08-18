"""Generate JSON values, JSON Schema and Python types for one OpenFOAM case."""

from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase


EXAMPLES_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = EXAMPLES_ROOT / "workflows" / "parametric_sweep" / "settings" / "base_case"
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "generated_base_case"


def main() -> None:
    case = OpenFOAMCase(CASE_PATH)
    artifacts = case.parser.export_schema(
        OUTPUT_DIR,
        name="BaseCase",
        sections=("constant", "system"),
        files={
            "constant": ["transportProperties"],
            "system": ["controlDict", "fvSchemes"],
        },
    )

    print(f"Values:      {artifacts.config}")
    print(f"JSON Schema: {artifacts.schema}")
    print(f"Python types: {artifacts.types}")


if __name__ == "__main__":
    main()
