"""Create typed configuration snapshots without modifying or running a case.

Run ``02_generate_case_schema.py`` before opening or executing this file.
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

from output.generated_base_case.types import CaseSettings
from pyRunOF.openfoam import OpenFOAMCase
from pyRunOF.sweep import ParametricSweep, SweepPoint


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = PROJECT_ROOT / "examples" / "workflows" / "parametric_sweep" / "settings" / "base_case"
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "sweep_settings"


def main() -> None:
    case = OpenFOAMCase(CASE_PATH)
    base_settings = cast(
        CaseSettings,
        case.parser.parse(
            sections=("constant", "system"),
            files={
                "constant": ["transportProperties"],
                "system": ["controlDict"],
            },
        ),
    )
    sweep = ParametricSweep(
        {"end_time": [50, 100], "viscosity": [1e-6, 2e-6]},
        mode="zip",
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def save_settings(point: SweepPoint) -> Path:
        settings = deepcopy(base_settings)
        settings["system"]["controlDict"]["endTime"] = point.parameters["end_time"]
        settings["constant"]["transportProperties"]["nu"] = point.parameters["viscosity"]
        destination = OUTPUT_DIR / f"{point.name}.json"
        destination.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        return destination

    for destination in sweep.run(save_settings, progress=True):
        print(f"Created: {destination}")


if __name__ == "__main__":
    main()
