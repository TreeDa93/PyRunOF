"""Prepare and run the Poiseuille-flow OpenFOAM example."""

from pathlib import Path

from pyRunOF.case import ModelConfigurator
from pyRunOF.openfoam import OpenFOAMCase

from data import BASE_CASE_NAME, PARAMETERS, SOLVER, TURBULENCE_MODEL


EXAMPLE_ROOT = Path(__file__).resolve().parent
SOURCE_CASE = EXAMPLE_ROOT / BASE_CASE_NAME
SOLUTION_CASE = EXAMPLE_ROOT / f"{BASE_CASE_NAME}_solved"


def main() -> None:
    """Copy, configure, mesh, and solve the example case."""
    configurator = ModelConfigurator(dir_path=EXAMPLE_ROOT)
    configurator.duplicate_case(SOURCE_CASE, SOLUTION_CASE, mode="rewrite")

    case = OpenFOAMCase(SOLUTION_CASE)
    case.system.set_controlDict(PARAMETERS)
    case.mesh.set_blockMesh(PARAMETERS)

    initial_values = case.initial_values.calcInitVal(
        PARAMETERS["A_var"],
        PARAMETERS["B_var"],
        PARAMETERS["Uin_var"],
        PARAMETERS["nu_var"],
    )
    case.initial_values.set_var(PARAMETERS, initial_values)

    case.constant.set_transportProp(PARAMETERS)
    case.constant.turbulent_model(turbulent_type=TURBULENCE_MODEL)

    case.mesh.run_blockMesh()
    case.runner.set_solver_name(SOLVER)
    case.runner.run()


if __name__ == "__main__":
    main()
