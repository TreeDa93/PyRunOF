from pathlib import Path
from unittest.mock import patch

import pytest

from pyRunOF import ConfigurationError, Run
from pyRunOF.additional_fun.auxiliary_functions import run_command


def test_common_command() -> None:
    runner = Run(solver="icoFoam")
    assert runner._collect_name_solver("general") == ["icoFoam"]


def test_parallel_command_has_no_trailing_colon() -> None:
    runner = Run(solver="pimpleFoam", mode="parallel", OF_core=4)
    assert runner._collect_name_solver("general") == [
        "mpirun",
        "-np",
        "4",
        "pimpleFoam",
        "-parallel",
    ]


def test_non_default_information_key_is_used() -> None:
    runner = Run(info_key="case_a", solver="icoFoam", mode="parallel", OF_core=3)
    assert runner._collect_name_solver("case_a")[2] == "3"


def test_solver_name_rejects_shell_syntax() -> None:
    runner = Run()
    with pytest.raises(ConfigurationError, match="executable"):
        runner.set_solver_name("icoFoam; rm -rf case")


def test_run_command_does_not_use_shell(tmp_path: Path) -> None:
    with patch("subprocess.run") as subprocess_run:
        subprocess_run.return_value = object()
        run_command(["solver", "--flag"], tmp_path)

    assert subprocess_run.call_args.args[0] == ["solver", "--flag"]
    assert subprocess_run.call_args.kwargs["check"] is True
    assert "shell" not in subprocess_run.call_args.kwargs
