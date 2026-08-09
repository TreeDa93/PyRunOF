"""Example integration test for a parametric OpenFOAM study.

By default the script only prepares cases and parameter snapshots.  Set
``TEST_MODE`` to ``False`` to run OpenFOAM commands as well.
"""

from pathlib import Path

from pyRunOF.case import ModelConfigurator
from pyRunOF.openfoam import OpenFOAMCase
from pyRunOF.sweep import ParametricSweep

from settings.data import BASE_PARAMETERS, OF_CORES, SOLVER, SWEEP_PARAMETERS


TEST_MODE = True
GENERATE_JSON_PARAMS = True
DELETE_SOLUTION_FOLDER = False
DELETE_CASES = False

TEST_ROOT = Path(__file__).resolve().parent
SOURCE_CASE = TEST_ROOT / "settings" / "base_case"
SOLUTION_ROOT = TEST_ROOT / "solution"


def prepare_case(sweep: ParametricSweep) -> None:
    """Create and configure one case for the current parameter set."""
    parameters = BASE_PARAMETERS | sweep.cur_data
    case_path = SOLUTION_ROOT / f"{SOURCE_CASE.name}_{sweep.cur_i}"

    configurator = ModelConfigurator(dir_path=TEST_ROOT)
    configurator.duplicate_case(SOURCE_CASE, case_path, mode="rewrite")

    case = OpenFOAMCase(case_path)
    case.system.set_controlDict(parameters)
    case.system.set_any_file(parameters, files=("decomposeParDict",))

    initial_values = case.initial_values.calcInitVal(
        parameters["A_var"],
        parameters["B_var"],
        parameters["Uin_var"],
        parameters["nu_var"],
    )
    parameters.update(initial_values)
    case.initial_values.set_var(parameters)

    case.constant.set_transportProp(parameters)
    case.constant.turbulent_model(turbulent_type="kOmega")
    case.mesh.set_blockMesh(parameters)

    case.runner.set_solver_name(SOLVER)
    case.runner.set_mode("parallel")
    case.runner.set_cores_OF(OF_CORES)

    if GENERATE_JSON_PARAMS:
        snapshot_path = SOLUTION_ROOT / f"params_{sweep.cur_i}"
        configurator.create_json_params(parameters, save_path=snapshot_path)

    if not TEST_MODE:
        case.mesh.run_blockMesh()
        case.mesh.run_decompose(what="OF")
        case.runner.run()


def main() -> None:
    configurator = ModelConfigurator(dir_path=TEST_ROOT)

    if DELETE_SOLUTION_FOLDER and SOLUTION_ROOT.exists():
        configurator.delete_folders([SOLUTION_ROOT], directory=TEST_ROOT)

    SOLUTION_ROOT.mkdir(exist_ok=True)
    if DELETE_CASES:
        configurator.delete_folders_by_words("base_case", directory=SOLUTION_ROOT)

    sweep = ParametricSweep(prepare_case)
    sweep.run(SWEEP_PARAMETERS, type_set="series")


if __name__ == "__main__":
    main()
