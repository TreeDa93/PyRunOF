"""Utilities for deterministic parametric studies."""

from __future__ import annotations

import itertools
from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from typing import Any

from tqdm import tqdm


class ParametricSweep:
    """Execute a callback for combinations of named parameter values."""

    VALID_MODES = {"all", "series", "special series"}

    def __init__(self, fun: Callable[[ParametricSweep], Any] | None = None):
        self.run_fun = fun
        self.cur_i = 0
        self.cur_data: dict[str, Any] = {}
        self.set: list[dict[str, Any]] = []
        self.n_iter = 0
        self.type_set = "all"

    def run(
        self,
        ps_params: Mapping[str, Sequence[Any]],
        fun: Callable[[ParametricSweep], Any] | None = None,
        update_vars: tuple[MutableMapping[str, Any], ...] | None = None,
        type_set: str = "special series",
    ) -> None:
        self._execute(ps_params, fun, update_vars, type_set, progress=False)

    def run_progress_bar(
        self,
        ps_params: Mapping[str, Sequence[Any]],
        fun: Callable[[ParametricSweep], Any] | None = None,
        update_vars: tuple[MutableMapping[str, Any], ...] | None = None,
        type_set: str = "special series",
    ) -> None:
        self._execute(ps_params, fun, update_vars, type_set, progress=True)

    def _execute(self, ps_params, fun, update_vars, type_set, *, progress: bool) -> None:
        self._prepare_ps_dict(ps_params, type_set=type_set)
        callback = fun if fun is not None else self.run_fun
        if not callable(callback):
            raise TypeError("fun must be callable")
        if update_vars is not None:
            self._validate_update_vars(update_vars)

        self.cur_i = 0
        values = tqdm(self.set, total=self.n_iter) if progress else self.set
        for index, current in enumerate(values, start=1):
            self.cur_i = index
            self.cur_data = current
            if update_vars is not None:
                self._update_variables(update_vars)
            callback(self)

    def get_cur_name(self, type_name: str = "index") -> str:
        if type_name == "index":
            return str(self.cur_i)
        return "".join(f"_{key}_{value}" for key, value in self.cur_data.items())

    def _prepare_ps_dict(self, ps_dict: Mapping[str, Sequence[Any]], type_set: str = "all") -> None:
        if type_set not in self.VALID_MODES:
            raise ValueError(f"type_set must be one of {sorted(self.VALID_MODES)}")
        if not isinstance(ps_dict, Mapping) or not ps_dict:
            raise ValueError("ps_params must be a non-empty mapping")

        keys = list(ps_dict)
        values = [list(ps_dict[key]) for key in keys]
        if any(not entries for entries in values):
            raise ValueError("each sweep parameter must contain at least one value")

        combinations: Iterable[tuple[Any, ...]]
        if type_set == "all":
            combinations = itertools.product(*values)
        else:
            if type_set == "series" and len({len(entries) for entries in values}) != 1:
                raise ValueError("series parameters must contain the same number of values")
            combinations = zip(*values, strict=type_set == "series")

        self.set = [dict(zip(keys, combination, strict=True)) for combination in combinations]
        self.n_iter = len(self.set)
        self.type_set = type_set

    @staticmethod
    def _validate_update_vars(update_vars: tuple[MutableMapping[str, Any], ...]) -> None:
        if not isinstance(update_vars, tuple):
            raise TypeError("update_vars must be a tuple of mutable mappings")
        if not all(isinstance(item, MutableMapping) for item in update_vars):
            raise TypeError("each update_vars item must be a mutable mapping")

    def _update_variables(self, update_vars: tuple[MutableMapping[str, Any], ...]) -> None:
        for data_dict in update_vars:
            data_dict.update(self.cur_data)
