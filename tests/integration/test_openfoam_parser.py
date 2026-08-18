
from pathlib import Path

from pyRunOF.openfoam import OpenFOAMCase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = PROJECT_ROOT / "examples" / "workflows" / "poiseuille_flow" / "PoiseuilleFlow"
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
    assert saved_path == OUTPUT_PATH

if __name__ == "__main__":
    test_parse_case()
