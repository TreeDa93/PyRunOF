import pytest

from pyRunOF import ParametricSweep


def test_all_combinations_are_executed_once() -> None:
    visited = []
    sweep = ParametricSweep(lambda current: visited.append(current.cur_data.copy()))

    sweep.run({"velocity": [1, 2], "model": ["k-e", "sst"]}, type_set="all")

    assert sweep.n_iter == 4
    assert [entry["velocity"] for entry in visited] == [1, 1, 2, 2]
    assert sweep.cur_i == 4


def test_repeated_run_resets_index() -> None:
    indices = []
    sweep = ParametricSweep(lambda current: indices.append(current.cur_i))

    sweep.run({"x": [1, 2]}, type_set="series")
    sweep.run({"x": [3]}, type_set="series")

    assert indices == [1, 2, 1]


def test_current_name_uses_current_data() -> None:
    names = []
    sweep = ParametricSweep(lambda current: names.append(current.get_cur_name("values")))
    sweep.run({"u": [5]}, type_set="all")
    assert names == ["_u_5"]


def test_series_requires_equal_lengths() -> None:
    with pytest.raises(ValueError, match="same number"):
        ParametricSweep().run({"x": [1, 2], "y": [3]}, fun=lambda _: None, type_set="series")


def test_invalid_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="type_set"):
        ParametricSweep().run({"x": [1]}, fun=lambda _: None, type_set="invalid")
