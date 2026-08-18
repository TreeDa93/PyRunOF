import pytest

from pyRunOF import ParametricSweep
from pyRunOF.sweep import SweepExecutionError, SweepPoint


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
    with pytest.raises(ValueError, match="mode"):
        ParametricSweep().run({"x": [1]}, fun=lambda _: None, type_set="invalid")


def test_new_api_returns_results_and_safe_names() -> None:
    sweep = ParametricSweep({"velocity": [1, 2], "model": ["k/e"]}, mode="product")

    results = sweep.run(lambda point: (point.name, point.parameters["velocity"]))

    assert results == [
        ("case-0001__velocity-1__model-k-e", 1),
        ("case-0002__velocity-2__model-k-e", 2),
    ]


def test_points_are_immutable_and_sweep_is_reusable() -> None:
    sweep = ParametricSweep({"x": [1, 2]})
    first = next(iter(sweep))
    assert isinstance(first, SweepPoint)
    with pytest.raises(TypeError):
        first.parameters["x"] = 4  # type: ignore[index]
    assert [point.index for point in sweep] == [1, 2]
    assert [point.index for point in sweep] == [1, 2]


def test_zip_rejects_different_lengths_and_zip_shortest_is_explicit() -> None:
    with pytest.raises(ValueError, match="same number"):
        ParametricSweep({"x": [1, 2], "y": [3]}, mode="zip")
    sweep = ParametricSweep({"x": [1, 2], "y": [3]}, mode="zip_shortest")
    assert sweep.total == 1
    assert len(list(sweep)) == 1


def test_execution_error_contains_point_context() -> None:
    sweep = ParametricSweep({"x": [1, 2]})

    with pytest.raises(SweepExecutionError, match="point 1") as raised:
        sweep.run(lambda point: 1 / 0)

    assert raised.value.point.parameters["x"] == 1
    assert isinstance(raised.value.__cause__, ZeroDivisionError)


def test_continue_policy_collects_errors() -> None:
    sweep = ParametricSweep({"x": [1, 2]})

    results = sweep.run(
        lambda point: point.parameters["x"] if point.index == 2 else 1 / 0,
        on_error="continue",
    )

    assert isinstance(results[0], SweepExecutionError)
    assert results[1] == 2


def test_large_product_is_not_materialized() -> None:
    sweep = ParametricSweep({f"p{i}": range(10) for i in range(10)})
    assert sweep.total == 10**10
    assert next(iter(sweep)).index == 1
