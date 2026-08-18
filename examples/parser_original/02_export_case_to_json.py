"""Export all supported dictionaries of an existing case to one JSON file."""

from pathlib import Path

from pyRunOF.openfoam import CaseParser


EXAMPLES_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = EXAMPLES_ROOT / "workflows" / "parametric_sweep" / "settings" / "base_case"
OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "base-case-config.json"


def main() -> None:
    parser = CaseParser(CASE_PATH)
    saved_path = parser.save(
        OUTPUT_PATH,
        sections=("constant", "system"),
        files={
            "constant": ["transportProperties"],
            "system": ["controlDict", "fvSolution"],
        },
    )

    print(f"Configuration exported to: {saved_path}")


if __name__ == "__main__":
    main()
