import sys
from pathlib import Path

from pyRunOF.additional_fun.auxiliary_functions import run_command


def test_run_command_streams_output_to_callback_and_log(tmp_path: Path) -> None:
    observed: list[str] = []

    result = run_command(
        [sys.executable, "-c", "print('iteration 1'); print('iteration 2')"],
        tmp_path,
        log_path="solver.log",
        output_callback=observed.append,
    )

    assert result.returncode == 0
    assert observed == ["iteration 1", "iteration 2"]
    assert (tmp_path / "solver.log").read_text(encoding="utf-8") == (
        "iteration 1\niteration 2\n"
    )
