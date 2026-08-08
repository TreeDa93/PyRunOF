"""Safe construction and execution of OpenFOAM solver commands."""

from __future__ import annotations

import re
import subprocess

from pyRunOF.additional_fun.auxiliary_functions import Priority, run_command
from pyRunOF.additional_fun.information import Information
from pyRunOF.exceptions import ConfigurationError

_EXECUTABLE_NAME = re.compile(r"^[A-Za-z0-9_.+-]+$")


class Run(Information):
    """Configure and run an OpenFOAM or coupled OpenFOAM/Elmer case."""

    def __init__(self, **optional_args):
        Information.__init_runner__(self, **optional_args)

    def __str__(self) -> str:
        return f"Run({self.info!r})"

    __repr__ = __str__

    def run(self, **options) -> subprocess.CompletedProcess[str]:
        info_key = self.get_key(options.get("info_key"))
        case_path = Priority.path(
            options.get("case_path"), self.info[info_key], path_key="case_path"
        )
        log_path = "log" if self.get_any_parameter("log", info_key=info_key) else None
        return run_command(
            self._collect_name_solver(info_key),
            case_path,
            log_path=log_path,
            timeout=options.get("timeout"),
        )

    def set_cores(self, coreOF: int = 4, coreElmer: int = 4, info_key=None) -> None:
        self.set_cores_OF(coreOF, info_key=info_key)
        self.set_cores_Elmer(coreElmer, info_key=info_key)

    def set_cores_OF(self, coreOF: int = 4, info_key=None) -> None:
        self.set_new_parameter(self._validate_cores(coreOF), info_key, "OF_core")

    def set_cores_Elmer(self, coreElmer: int = 4, info_key=None) -> None:
        self.set_new_parameter(self._validate_cores(coreElmer), info_key, "E_core")

    def set_solver_name(self, solver_name: str = "pimpleFoam", info_key=None) -> None:
        self.set_new_parameter(self._validate_executable(solver_name), info_key, "solver")

    def set_mode(self, mode: str = "common", info_key=None) -> None:
        if mode not in {"common", "parallel", "EOF"}:
            raise ConfigurationError("mode must be 'common', 'parallel', or 'EOF'")
        self.set_new_parameter(mode, info_key, "mode")

    def set_pyFoam(self, pyFoam: bool = False, info_key=None) -> None:
        self.set_new_parameter(bool(pyFoam), info_key, "pyFoam")

    def set_log_flag(self, log_flag: bool = False, info_key=None) -> None:
        self.set_new_parameter(bool(log_flag), info_key, "log")

    def _collect_name_solver(self, info_key: str) -> list[str]:
        mode = self.get_any_parameter("mode", info_key=info_key)
        solver = self._validate_executable(self.get_any_parameter("solver", info_key=info_key))
        if mode == "common":
            command = [solver]
        elif mode == "parallel":
            cores = self._validate_cores(self.get_any_parameter("OF_core", info_key=info_key))
            command = ["mpirun", "-np", str(cores), solver, "-parallel"]
        elif mode == "EOF":
            of_cores = self._validate_cores(self.get_any_parameter("OF_core", info_key=info_key))
            e_cores = self._validate_cores(self.get_any_parameter("E_core", info_key=info_key))
            command = [
                "mpirun",
                "-np",
                str(of_cores),
                solver,
                "-parallel",
                ":",
                "-np",
                str(e_cores),
                "ElmerSolver_mpi",
            ]
        else:
            raise ConfigurationError(f"Unknown run mode: {mode!r}")

        if self.get_any_parameter("pyFoam", info_key=info_key):
            command.insert(0, "pyFoamPlotRunner.py")
        self.set_new_parameter(command, info_key, "run command")
        return command

    @staticmethod
    def _validate_executable(name: str) -> str:
        if not isinstance(name, str) or not _EXECUTABLE_NAME.fullmatch(name):
            raise ConfigurationError(f"Invalid executable name: {name!r}")
        return name

    @staticmethod
    def _validate_cores(value: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ConfigurationError("core count must be a positive integer")
        return value
