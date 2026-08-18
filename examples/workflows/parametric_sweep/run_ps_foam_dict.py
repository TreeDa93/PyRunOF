"""Parametric study configured through ``foamDictionary``.

Unlike ``run_ps.py``, this example applies all case settings through
``CaseParser.apply`` instead of the historical text-replacement helpers.
OpenFOAM (and its ``foamDictionary`` command) must be available even in test
mode; solver and mesh commands are skipped while ``TEST_MODE`` is true.
"""

from pathlib import Path

from pyRunOF.case import ModelConfigurator
from pyRunOF.openfoam import OpenFOAMCase
from pyRunOF.sweep import ParametricSweep, SweepPoint

from settings.data import BASE_PARAMETERS, OF_CORES, SOLVER, SWEEP_PARAMETERS


TEST_MODE = True
GENERATE_JSON_PARAMS = True
DELETE_SOLUTION_FOLDER = False
WORKERS = 2
DISPLAY = "all"

TEST_ROOT = Path(__file__).resolve().parent
SOURCE_CASE = TEST_ROOT / "settings" / "base_case"
SOLUTION_ROOT = TEST_ROOT / "solution_foam_dict"


def calculate_initial_values(parameters: dict[str, float]) -> dict[str, float]:
    """Calculate turbulence inlet values for the current sweep point."""
    height = parameters["A_var"]
    width = parameters["B_var"]
    velocity = parameters["Uin_var"]
    viscosity = parameters["nu_var"]

    hydraulic_diameter = 2 * height * width / (height + width)
    reynolds = velocity * hydraulic_diameter / viscosity
    intensity = 0.16 * reynolds ** (-0.125)
    length_scale = hydraulic_diameter * intensity
    kinetic_energy = 1.5 * (intensity * velocity) ** 2
    omega = kinetic_energy**0.5 / (0.09**0.25 * length_scale)
    epsilon = 0.09**0.75 * kinetic_energy**1.5 / length_scale

    return {
        "Dh_var": hydraulic_diameter,
        "Re_var": reynolds,
        "Ical_var": intensity,
        "L_var": length_scale,
        "k_var": kinetic_energy,
        "omega_var": omega,
        "ep_var": epsilon,
    }


def build_case_settings(parameters: dict[str, float]) -> dict:
    """Map sweep parameters to exact OpenFOAM dictionary entries."""
    velocity = parameters["Uin_var"]
    velocity_field = f"uniform ({velocity} 0 0)"

    return {
        "initial_conditions": {
            "U": {
                "Uinlet": [velocity, 0, 0],
                "internalField": velocity_field,
                "boundaryField": {"inlet": {"value": velocity_field}},
            },
            "k": {
                "Ical": parameters["Ical_var"],
                "kp": parameters["k_var"],
            },
            "omega": {
                "L1": parameters["L_var"],
                "omegap": parameters["omega_var"],
            },
            "epsilon": {
                "ep": parameters["ep_var"],
                "L1": parameters["L_var"],
            },
        },
        "constant": {
            "transportProperties": {
                "nu": f"nu [0 2 -1 0 0 0 0] {parameters['nu_var']}",
                "rho": f"rho [1 -3 0 0 0 0 0] {parameters['rho_var']}",
            },
            "turbulenceProperties": {
                "simulationType": "RAS",
                "RAS": {"RASModel": "kOmega"},
            },
        },
        "system": {
            "controlDict": {
                "startTime": parameters["startTime_var"],
                "endTime": parameters["endTime_var"],
            },
            "decomposeParDict": {
                "numberOfSubdomains": OF_CORES,
            },
            "blockMeshDict": {
                "L": parameters["Lx_var"],
                "A": parameters["A_var"],
                "B": parameters["B_var"],
                "hx": parameters["hx_var"],
                "hy": parameters["hy_var"],
                "hz": parameters["hz_var"],
            },
        },
    }


def prepare_case(point: SweepPoint) -> Path:
    """Copy and configure one case for the current parameter set."""
    parameters = BASE_PARAMETERS | point.parameters
    parameters.update(calculate_initial_values(parameters))
    case_path = SOLUTION_ROOT / f"{SOURCE_CASE.name}_{point.index}"
    point.log(f"preparing {case_path}")

    configurator = ModelConfigurator(dir_path=TEST_ROOT)
    configurator.duplicate_case(SOURCE_CASE, case_path, mode="rewrite")

    case = OpenFOAMCase(case_path)
    report = case.parser.apply(build_case_settings(parameters))
    point.log(f"updated {report['updated']} entries")

    case.runner.set_solver_name(SOLVER)
    case.runner.set_mode("parallel")
    case.runner.set_cores_OF(OF_CORES)

    if GENERATE_JSON_PARAMS:
        snapshot_path = SOLUTION_ROOT / f"params_{point.index}.json"
        configurator.create_json_params(parameters, save_path=snapshot_path)

    if not TEST_MODE:
        case.mesh.run_blockMesh()
        case.mesh.run_decompose(what="OF")
        case.runner.run(output_callback=point.log)
    return case_path


def main() -> None:
    configurator = ModelConfigurator(dir_path=TEST_ROOT)
    if DELETE_SOLUTION_FOLDER and SOLUTION_ROOT.exists():
        configurator.delete_folders([SOLUTION_ROOT], directory=TEST_ROOT)

    SOLUTION_ROOT.mkdir(exist_ok=True)
    sweep = ParametricSweep(SWEEP_PARAMETERS, mode="zip")
    sweep.run(
        prepare_case,
        workers=WORKERS,
        display=DISPLAY,
        journal_path=SOLUTION_ROOT / "sweep-journal.json",
        on_error="continue",
    )


if __name__ == "__main__":
    main()
