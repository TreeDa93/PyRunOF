"""Use generated ``TypedDict`` definitions for IDE key suggestions.

Run ``04_generate_case_schema.py`` once before opening or executing this example.
"""

from pathlib import Path
from typing import cast

from output.generated_base_case.types import CaseSettings
from pyRunOF.openfoam import OpenFOAMCase


EXAMPLES_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = EXAMPLES_ROOT / "workflows" / "parametric_sweep" / "settings" / "base_case"


def main() -> None:
    case = OpenFOAMCase(CASE_PATH)
    settings = cast(
        CaseSettings,
        case.parser.parse(
            sections=("constant", "system"),
            files={
                "constant": ["transportProperties"],
                "system": ["controlDict", "fvSchemes"],
            },
        ),
    )

    # IDE completion is available after each ["..."] access.
    application = settings["system"]["controlDict"]["application"]
    end_time = settings["system"]["controlDict"]["endTime"]
    viscosity = settings["constant"]["transportProperties"]["nu"]

    print(f"Solver: {application}")
    print(f"End time: {end_time}")
    print(f"Kinematic viscosity: {viscosity}")


if __name__ == "__main__":
    main()
