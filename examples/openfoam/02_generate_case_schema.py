"""Generate values, JSON Schema, and Python types for an OpenFOAM case."""

from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = PROJECT_ROOT / "examples" / "workflows" / "parametric_sweep" / "settings" / "base_case"
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

    print(f"Configuration values: {artifacts.config}")
    print(f"Editor schema:       {artifacts.schema}")
    print(f"Python IDE types:    {artifacts.types}")


if __name__ == "__main__":
    main()
