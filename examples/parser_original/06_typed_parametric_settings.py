"""Create typed configuration snapshots for a small parametric study.

Run ``04_generate_case_schema.py`` first. This example only writes JSON snapshots;
it does not modify the source OpenFOAM case or start a solver.
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

from output.generated_base_case.types import CaseSettings
from pyRunOF.openfoam import OpenFOAMCase
from pyRunOF.sweep import ParametricSweep, SweepPoint


EXAMPLES_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = EXAMPLES_ROOT / "workflows" / "parametric_sweep" / "settings" / "base_case"
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
        {
            "end_time": [50, 100],
            "viscosity": [1e-6, 2e-6],
        },
        mode="zip",
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def save_point(point: SweepPoint) -> Path:
        settings = deepcopy(base_settings)
        settings["system"]["controlDict"]["endTime"] = point.parameters["end_time"]
        settings["constant"]["transportProperties"]["nu"] = point.parameters["viscosity"]

        destination = OUTPUT_DIR / f"{point.name}.json"
        destination.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return destination

    for path in sweep.run(save_point, progress=True):
        print(f"Created: {path}")


if __name__ == "__main__":
    main()
