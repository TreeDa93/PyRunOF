"""Typed configuration shared by PyRunOF components."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


def _path_or_none(value: str | Path | None) -> Path | None:
    return None if value is None else Path(value)


@dataclass
class CaseConfig:
    """Configuration for one named simulation case.

    ``paths`` and ``names`` hold extensible user-defined values while common
    runtime settings live in ``parameters``.  This replaces the several
    incompatible shapes formerly created by ``Information``.
    """

    key: str = "general"
    case_path: Path | None = None
    paths: dict[str, Path | None] = field(default_factory=dict)
    names: dict[str, str | None] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.case_path = _path_or_none(self.case_path)
        self.paths = {name: _path_or_none(path) for name, path in self.paths.items()}
        if self.case_path is not None:
            self.paths.setdefault("case_path", self.case_path)

    @classmethod
    def from_mapping(cls, key: str, values: Mapping[str, Any]) -> CaseConfig:
        paths = dict(values.get("paths", {}))
        names = dict(values.get("case_names", values.get("names", {})))
        case_path = values.get("case_path", paths.get("case_path", paths.get("path")))
        reserved = {"paths", "case_names", "names", "case_path"}
        parameters = {name: value for name, value in values.items() if name not in reserved}
        return cls(key, case_path, paths, names, parameters)

    def to_mapping(self) -> dict[str, Any]:
        """Return the transitional dictionary representation used by old APIs."""
        values: dict[str, Any] = {
            "paths": self.paths,
            "case_names": self.names,
            **self.parameters,
        }
        if self.case_path is not None:
            values["case_path"] = self.case_path
        return values

    def path(self, key: str = "case_path") -> Path:
        value = self.case_path if key == "case_path" else self.paths.get(key)
        if value is None:
            raise KeyError(f"Path {key!r} is not configured for case {self.key!r}")
        return Path(value)

    def name(self, key: str) -> str:
        value = self.names.get(key)
        if value is None:
            raise KeyError(f"Name {key!r} is not configured for case {self.key!r}")
        return value

