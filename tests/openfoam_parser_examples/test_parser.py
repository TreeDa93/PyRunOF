
from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase

TESTS_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = TESTS_ROOT / "PoiseuilleFlow" / "PoiseuilleFlow"
OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "base-case-config.json"

def test_parse_case():
    case = OpenFOAMCase(CASE_PATH)
    settings = case.parser.parse(sections="system")
    print(f"Case: {settings['case']['name']}")
    print(f"Parsed system settings: {settings['system']}")
    saved_path = case.parser.save(
        OUTPUT_PATH,
        sections=("constant", "system"),
        files={
            "constant": ["transportProperties"],
            "system": ["controlDict", "fvSolution"],
        },
    )

if __name__ == "__main__":
    test_parse_case()