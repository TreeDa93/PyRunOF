"""Parametric-study planning and execution."""

from __future__ import annotations

import itertools
import math
import re
import warnings
from collections.abc import Callable, Iterator, Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Literal

from tqdm import tqdm

SweepMode = Literal["product", "zip", "zip_shortest"]
ErrorPolicy = Literal["raise", "continue"]
_LEGACY_MODES = {"all": "product", "series": "zip", "special series": "zip_shortest"}
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")


def _safe_part(value: Any) -> str:
    part = _SAFE_NAME.sub("-", str(value).strip()).strip("-.")
    return part or "value"


@dataclass(frozen=True, slots=True)
class SweepPoint:
    """One immutable point in a parametric study."""

    index: int
    parameters: Mapping[str, Any]

    @property
    def name(self) -> str:
        """A deterministic, filesystem-safe name containing index and parameters."""
        values = "__".join(
            f"{_safe_part(key)}-{_safe_part(value)}" for key, value in self.parameters.items()
        )
        return f"case-{self.index:04d}__{values}" if values else f"case-{self.index:04d}"


class SweepExecutionError(RuntimeError):
    """A callback failure enriched with the point that caused it."""

    def __init__(self, point: SweepPoint, cause: BaseException):
        self.point = point
        self.cause = cause
        super().__init__(
            f"Parametric sweep failed at point {point.index} "
            f"with parameters {dict(point.parameters)!r}: {cause}"
        )


class ParametricSweep:
    """Define, inspect and execute a deterministic parametric study.

    New code passes parameters to the constructor and receives a
    :class:`SweepPoint` in its callback. The historical ``ParametricSweep(fun)``
    and ``run(parameters, type_set=...)`` forms remain available temporarily.
    """

    VALID_MODES = {"product", "zip", "zip_shortest"}

    def __init__(
        self,
        parameters: Mapping[str, Sequence[Any]] | Callable[[ParametricSweep], Any] | None = None,
        *,
        mode: SweepMode = "product",
    ) -> None:
        self._legacy_callback: Callable[[ParametricSweep], Any] | None = None
        if callable(parameters):
            self._legacy_callback = parameters
            parameters = None
        self._parameters: dict[str, tuple[Any, ...]] = {}
        self.mode: SweepMode = self._normalize_mode(mode)
        self.current_point: SweepPoint | None = None
        if parameters is not None:
            self.configure(parameters, mode=mode)

    def configure(
        self, parameters: Mapping[str, Sequence[Any]], *, mode: SweepMode | str | None = None
    ) -> ParametricSweep:
        """Validate and store a reusable sweep plan."""
        if not isinstance(parameters, Mapping) or not parameters:
            raise ValueError("parameters must be a non-empty mapping")
        prepared: dict[str, tuple[Any, ...]] = {}
        for key, entries in parameters.items():
            if not isinstance(key, str) or not key:
                raise TypeError("parameter names must be non-empty strings")
            if isinstance(entries, (str, bytes)) or not isinstance(entries, Sequence):
                raise TypeError(f"values for parameter {key!r} must be a sequence")
            values = tuple(entries)
            if not values:
                raise ValueError(f"parameter {key!r} must contain at least one value")
            prepared[key] = values
        selected_mode = self.mode if mode is None else self._normalize_mode(mode)
        if selected_mode == "zip" and len({len(values) for values in prepared.values()}) != 1:
            raise ValueError("zip mode requires all parameters to contain the same number of values")
        self._parameters = prepared
        self.mode = selected_mode
        self.current_point = None
        return self

    @property
    def parameters(self) -> Mapping[str, Sequence[Any]]:
        return MappingProxyType(self._parameters)

    @property
    def total(self) -> int:
        if not self._parameters:
            return 0
        lengths = [len(values) for values in self._parameters.values()]
        return math.prod(lengths) if self.mode == "product" else min(lengths)

    def __len__(self) -> int:
        return self.total

    def __iter__(self) -> Iterator[SweepPoint]:
        if not self._parameters:
            raise RuntimeError("sweep parameters are not configured")
        keys = tuple(self._parameters)
        values = tuple(self._parameters.values())
        combinations = itertools.product(*values) if self.mode == "product" else zip(*values)
        for index, combination in enumerate(combinations, start=1):
            data = MappingProxyType(dict(zip(keys, combination, strict=True)))
            yield SweepPoint(index, data)

    def run(
        self,
        parameters: Mapping[str, Sequence[Any]] | Callable[[SweepPoint], Any] | None = None,
        callback: Callable[[SweepPoint], Any] | None = None,
        *,
        progress: bool = False,
        mode: SweepMode | str | None = None,
        on_error: ErrorPolicy = "raise",
        fun: Callable[[ParametricSweep], Any] | None = None,
        update_vars: tuple[MutableMapping[str, Any], ...] | None = None,
        type_set: str | None = None,
    ) -> list[Any | SweepExecutionError]:
        """Execute the study and return one callback result per attempted point."""
        legacy_call = False
        if callable(parameters):
            if callback is not None:
                raise TypeError("callback was provided twice")
            callback = parameters
            parameters = None
        elif parameters is not None:
            legacy_call = True
            self.configure(parameters, mode=type_set or mode or "special series")
        elif mode is not None or type_set is not None:
            if not self._parameters:
                raise RuntimeError("sweep parameters are not configured")
            self.configure(self._parameters, mode=type_set or mode)
        if fun is not None:
            if callback is not None:
                raise TypeError("use either callback or fun, not both")
            callback = fun  # type: ignore[assignment]
            legacy_call = True
        if callback is None and self._legacy_callback is not None:
            callback = self._legacy_callback  # type: ignore[assignment]
            legacy_call = True
        if not callable(callback):
            raise TypeError("callback must be callable")
        if on_error not in {"raise", "continue"}:
            raise ValueError("on_error must be 'raise' or 'continue'")
        if update_vars is not None:
            self._validate_update_vars(update_vars)
            warnings.warn(
                "update_vars is deprecated; merge point.parameters in the callback instead",
                DeprecationWarning,
                stacklevel=2,
            )
        points = tqdm(iter(self), total=self.total) if progress else iter(self)
        results: list[Any | SweepExecutionError] = []
        self.current_point = None
        for point in points:
            self.current_point = point
            if update_vars is not None:
                for target in update_vars:
                    target.update(point.parameters)
            try:
                result = callback(self if legacy_call else point)  # type: ignore[arg-type]
            except Exception as exc:
                error = SweepExecutionError(point, exc)
                if on_error == "raise":
                    raise error from exc
                results.append(error)
            else:
                results.append(result)
        return results

    def run_iter(
        self, callback: Callable[[SweepPoint], Any], *, on_error: ErrorPolicy = "raise"
    ) -> Iterator[Any | SweepExecutionError]:
        """Execute lazily, yielding each callback result as soon as it is available."""
        if not callable(callback):
            raise TypeError("callback must be callable")
        if on_error not in {"raise", "continue"}:
            raise ValueError("on_error must be 'raise' or 'continue'")
        for point in self:
            self.current_point = point
            try:
                yield callback(point)
            except Exception as exc:
                error = SweepExecutionError(point, exc)
                if on_error == "raise":
                    raise error from exc
                yield error

    def run_progress_bar(self, *args: Any, **kwargs: Any) -> list[Any | SweepExecutionError]:
        warnings.warn(
            "run_progress_bar() is deprecated; use run(..., progress=True)",
            DeprecationWarning,
            stacklevel=2,
        )
        kwargs["progress"] = True
        return self.run(*args, **kwargs)

    @property
    def cur_i(self) -> int:
        return 0 if self.current_point is None else self.current_point.index

    @property
    def cur_data(self) -> dict[str, Any]:
        return {} if self.current_point is None else dict(self.current_point.parameters)

    @property
    def n_iter(self) -> int:
        return self.total

    @property
    def type_set(self) -> str:
        return self.mode

    @property
    def set(self) -> list[dict[str, Any]]:
        warnings.warn(
            "set is deprecated; iterate over ParametricSweep instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return [dict(point.parameters) for point in self]

    def get_cur_name(self, type_name: str = "index") -> str:
        if self.current_point is None:
            raise RuntimeError("the sweep has not started")
        if type_name == "index":
            return str(self.current_point.index)
        if type_name in {"values", "parameters"}:
            return "".join(
                f"_{_safe_part(key)}_{_safe_part(value)}"
                for key, value in self.current_point.parameters.items()
            )
        raise ValueError("type_name must be 'index', 'values', or 'parameters'")

    @classmethod
    def _normalize_mode(cls, mode: str) -> SweepMode:
        if mode in _LEGACY_MODES:
            warnings.warn(
                f"mode {mode!r} is deprecated; use {_LEGACY_MODES[mode]!r}",
                DeprecationWarning,
                stacklevel=3,
            )
            mode = _LEGACY_MODES[mode]
        if mode not in cls.VALID_MODES:
            raise ValueError(f"mode must be one of {sorted(cls.VALID_MODES)}")
        return mode  # type: ignore[return-value]

    @staticmethod
    def _validate_update_vars(update_vars: tuple[MutableMapping[str, Any], ...]) -> None:
        if not isinstance(update_vars, tuple):
            raise TypeError("update_vars must be a tuple of mutable mappings")
        if not all(isinstance(item, MutableMapping) for item in update_vars):
            raise TypeError("each update_vars item must be a mutable mapping")


__all__ = ["ParametricSweep", "SweepExecutionError", "SweepPoint"]
