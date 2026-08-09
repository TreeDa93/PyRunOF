"""Copy a case and apply selected settings without changing the source case."""

from pathlib import Path

from pyRunOF.case import ModelConfigurator
from pyRunOF.openfoam import OpenFOAMCase


TESTS_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CASE = TESTS_ROOT / "paralle_test" / "pitzDaily"
TARGET_CASE = Path(__file__).resolve().parent / "output" / "pitzDaily_modified"

CHANGES = {
    "initial_conditions": {
        "U": {
            "boundaryField": {
                "inlet": {
                    "value": "uniform (2 0 0)",
                }
            }
        }
    },
    "system": {
        "controlDict": {
            "endTime": 0.5,
            "writeInterval": 0.02,
            "maxCo": 1,
        }
    },
}


def main() -> None:
    configurator = ModelConfigurator(dir_path=TESTS_ROOT)
    configurator.duplicate_case(SOURCE_CASE, TARGET_CASE, mode="rewrite")

    target = OpenFOAMCase(TARGET_CASE)
    report = target.parser.apply(CHANGES)
    exported_path = target.parser.save("case-config.json")

    print(f"Updated values: {report['updated']}")
    print(f"Modified case: {target.path}")
    print(f"Resulting configuration: {exported_path}")


if __name__ == "__main__":
    main()
