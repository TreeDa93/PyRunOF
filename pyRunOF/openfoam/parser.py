"""Export OpenFOAM case dictionaries to a single JSON document."""

from __future__ import annotations

import json
import shlex
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tqdm.auto import tqdm

from pyRunOF.additional_fun.auxiliary_functions import run_command
from pyRunOF.exceptions import CommandExecutionError, ConfigurationError, UnsafePathError
from pyRunOF.openfoam.schema import (
    CaseSchemaArtifacts,
    build_json_schema,
    generate_typed_dicts,
    normalize_type_name,
)

CommandRunner = Callable[..., Any]
SectionSelection = str | Iterable[str]

SECTION_FOLDERS: dict[str, tuple[str, set[str]]] = {
    "initial_conditions": ("0", set()),
    "constant": ("constant", {"polyMesh"}),
    "system": ("system", set()),
}


class CaseParser:
    """Parse OpenFOAM dictionaries using the installed ``foamDictionary`` utility."""

    def __init__(self, case_path: str | Path, *, command_runner: CommandRunner = run_command):
        self.case_path = Path(case_path).expanduser().resolve()
        self._run_command = command_runner

    def parse(
        self,
        *,
        strict: bool = True,
        sections: SectionSelection = "all",
        parse_kind: str | None = None,
        files: Mapping[str, Iterable[str]] | None = None,
        progress: bool = True,
    ) -> dict[str, Any]:
        """Return settings from selected case sections.

        Every regular file is parsed recursively. ``constant/polyMesh`` is
        excluded because mesh topology is not case configuration. ``sections``
        accepts one section name, an iterable of names, or ``"all"``. ``files``
        can restrict each section further to selected relative file names. Set
        ``progress=False`` to suppress the file progress bar and ETA.

        """
        if not self.case_path.is_dir():
            raise FileNotFoundError(f"OpenFOAM case does not exist: {self.case_path}")

        if parse_kind is not None:
            if sections != "all":
                raise ValueError("Use either sections or parse_kind, not both")
            sections = parse_kind
        selected_sections = self._normalize_sections(sections)
        selected_files = self._normalize_files(files)
        unused_file_filters = set(selected_files).difference(selected_sections)
        if unused_file_filters:
            names = ", ".join(sorted(unused_file_filters))
            raise ValueError(f"File filters provided for unselected sections: {names}")

        section_plans = []
        for section in selected_sections:
            folder, excluded_directories = SECTION_FOLDERS[section]
            root = self.case_path / folder
            paths = (
                self._section_files(root, excluded_directories, selected_files.get(section))
                if root.is_dir()
                else []
            )
            section_plans.append((section, folder, paths))

        parsed_sections = {}
        total_files = sum(len(paths) for _, _, paths in section_plans)
        with tqdm(
            total=total_files,
            desc="Parsing OpenFOAM case",
            unit="file",
            dynamic_ncols=True,
            disable=not progress,
            bar_format=(
                "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} "
                "[прошло {elapsed}, осталось {remaining}] {postfix}"
            ),
        ) as progress_bar:
            for section, folder, paths in section_plans:
                def report_file(relative_path: Path) -> None:
                    progress_bar.set_postfix_str(f"file={relative_path}", refresh=True)
                    progress_bar.update(1)

                parsed_sections[section] = self._parse_section(
                    folder,
                    paths=paths,
                    strict=strict,
                    on_file_parsed=report_file,
                )

        return {
            "schema_version": 1,
            "case": {"name": self.case_path.name},
            **parsed_sections,
        }

    def save(
        self,
        destination: str | Path | None = None,
        *,
        strict: bool = True,
        indent: int = 2,
        sections: SectionSelection = "all",
        files: Mapping[str, Iterable[str]] | None = None,
        progress: bool = True,
    ) -> Path:
        """Parse the case and write a UTF-8 JSON file."""
        destination = Path(destination or self.case_path / "case-config.json")
        if not destination.is_absolute():
            destination = self.case_path / destination
        data = self.parse(
            strict=strict,
            sections=sections,
            files=files,
            progress=progress,
        )
        data["generated_at"] = datetime.now(timezone.utc).isoformat()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8"
        )
        return destination

    def export_schema(
        self,
        output: str | Path,
        *,
        name: str | None = None,
        strict: bool = True,
        indent: int = 2,
        sections: SectionSelection = "all",
        files: Mapping[str, Iterable[str]] | None = None,
        progress: bool = True,
    ) -> CaseSchemaArtifacts:
        """Export values, JSON Schema and importable ``TypedDict`` definitions.

        Relative output paths are resolved from the current working directory. The
        generated schema suggests entries found in this case while still allowing
        custom OpenFOAM keys.
        """
        directory = Path(output).expanduser().resolve()
        directory.mkdir(parents=True, exist_ok=True)

        data = self.parse(
            strict=strict,
            sections=sections,
            files=files,
            progress=progress,
        )
        data["generated_at"] = datetime.now(timezone.utc).isoformat()
        schema_name = normalize_type_name(name or self.case_path.name)

        config_path = directory / "config.json"
        schema_path = directory / "schema.json"
        types_path = directory / "types.py"
        config_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8"
        )
        schema_path.write_text(
            json.dumps(
                build_json_schema(data, title=f"{schema_name}Settings"),
                ensure_ascii=False,
                indent=indent,
            )
            + "\n",
            encoding="utf-8",
        )
        types_path.write_text(
            generate_typed_dicts(data, name=schema_name), encoding="utf-8"
        )
        return CaseSchemaArtifacts(directory, config_path, schema_path, types_path)

    def apply(
        self,
        settings: Mapping[str, Any] | str | Path,
        *,
        strict: bool = True,
    ) -> dict[str, Any]:
        """Apply parsed settings to this case through ``foamDictionary``.

        ``settings`` may be the dictionary returned by :meth:`parse` or the
        path to a JSON file created by :meth:`save`. Only the recognized case
        sections are processed; metadata is ignored.
        """
        data = self._load_settings(settings)
        section_folders = {
            "initial_conditions": "0",
            "constant": "constant",
            "system": "system",
        }
        report: dict[str, Any] = {"updated": 0, "errors": []}
        for section, folder in section_folders.items():
            files = data.get(section, {})
            if not isinstance(files, Mapping):
                raise ConfigurationError(f"Section {section!r} must be a JSON object")
            for file_name, entries in files.items():
                try:
                    relative_path = self._validate_target(folder, str(file_name))
                    if not isinstance(entries, Mapping):
                        raise ConfigurationError(
                            f"Settings for {section}/{file_name} must be a JSON object"
                        )
                    report["updated"] += self._apply_entries(relative_path, entries)
                except (CommandExecutionError, ConfigurationError, OSError, UnsafePathError) as exc:
                    if strict:
                        raise
                    report["errors"].append({"file": f"{folder}/{file_name}", "error": str(exc)})
        return report

    @staticmethod
    def _normalize_sections(sections: SectionSelection) -> tuple[str, ...]:
        if sections == "all":
            return tuple(SECTION_FOLDERS)
        if isinstance(sections, str):
            selected = (sections,)
        else:
            selected = tuple(dict.fromkeys(sections))
        if not selected:
            raise ValueError("At least one section must be selected")
        unknown = set(selected).difference(SECTION_FOLDERS)
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"Unknown case sections: {names}")
        return selected

    @staticmethod
    def _normalize_files(
        files: Mapping[str, Iterable[str]] | None,
    ) -> dict[str, set[str]]:
        if files is None:
            return {}
        unknown = set(files).difference(SECTION_FOLDERS)
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"File filters contain unknown sections: {names}")
        normalized: dict[str, set[str]] = {}
        for section, names in files.items():
            if isinstance(names, str):
                normalized[section] = {names}
            else:
                normalized[section] = {str(name) for name in names}
        return normalized

    @staticmethod
    def _load_settings(settings: Mapping[str, Any] | str | Path) -> Mapping[str, Any]:
        if isinstance(settings, Mapping):
            return settings
        path = Path(settings)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigurationError(f"Invalid JSON settings file: {path}") from exc
        if not isinstance(data, Mapping):
            raise ConfigurationError("The root JSON value must be an object")
        return data

    def _validate_target(self, folder: str, file_name: str) -> Path:
        relative_name = Path(file_name)
        if relative_name.is_absolute() or ".." in relative_name.parts:
            raise UnsafePathError(f"Unsafe case dictionary path: {file_name!r}")
        if folder == "constant" and "polyMesh" in relative_name.parts:
            raise UnsafePathError("constant/polyMesh cannot be changed by CaseParser")

        relative_path = Path(folder) / relative_name
        target = self.case_path / relative_path
        root = (self.case_path / folder).resolve()
        resolved = target.resolve()
        if not resolved.is_relative_to(root):
            raise UnsafePathError(f"Dictionary is outside the case section: {file_name!r}")
        if not target.is_file():
            raise FileNotFoundError(f"OpenFOAM dictionary does not exist: {target}")
        return relative_path

    def _apply_entries(
        self, relative_path: Path, entries: Mapping[str, Any], prefix: str = ""
    ) -> int:
        updated = 0
        for key, value in entries.items():
            if key in {"FoamFile", "_parse_error"}:
                continue
            entry = f"{prefix}/{key}" if prefix else str(key)
            if isinstance(value, Mapping):
                updated += self._apply_entries(relative_path, value, entry)
                continue
            command = [
                "foamDictionary",
                "-entry",
                entry,
                "-set",
                self._format_value(value),
                str(relative_path),
            ]
            self._run_command(command, self.case_path, capture_output=True)
            updated += 1
        return updated

    @classmethod
    def _format_value(cls, value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            raise ConfigurationError("OpenFOAM values cannot be null")
        if isinstance(value, (int, float, str)):
            return str(value) if value != "" else '""'
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            return "(" + " ".join(cls._format_value(item) for item in value) + ")"
        raise ConfigurationError(f"Unsupported OpenFOAM value type: {type(value).__name__}")

    def _parse_section(
        self,
        folder: str,
        *,
        paths: Sequence[Path],
        strict: bool,
        on_file_parsed: Callable[[Path], Any] | None = None,
    ) -> dict[str, Any]:
        root = self.case_path / folder
        result: dict[str, Any] = {}
        for path in paths:
            relative_case_path = path.relative_to(self.case_path)
            key = str(path.relative_to(root))
            try:
                result[key] = self._parse_dictionary(relative_case_path)
            except (CommandExecutionError, OSError, ValueError) as exc:
                if strict:
                    raise
                result[key] = {"_parse_error": str(exc)}
            finally:
                if on_file_parsed is not None:
                    on_file_parsed(relative_case_path)

        return result

    @staticmethod
    def _section_files(
        root: Path,
        excluded_directories: set[str],
        included_files: set[str] | None,
    ) -> list[Path]:
        if included_files is not None:
            paths = []
            for file_name in sorted(included_files):
                relative_path = Path(file_name)
                if relative_path.is_absolute() or ".." in relative_path.parts:
                    raise UnsafePathError(f"Unsafe case dictionary path: {file_name!r}")
                if any(part in excluded_directories for part in relative_path.parts[:-1]):
                    continue
                path = root / relative_path
                if not path.is_file():
                    raise FileNotFoundError(f"OpenFOAM dictionary does not exist: {path}")
                paths.append(path)
            return paths

        paths = []
        for directory, directory_names, file_names in root.walk():
            directory_names[:] = sorted(
                name for name in directory_names if name not in excluded_directories
            )
            paths.extend(
                directory / name for name in sorted(file_names) if not name.startswith(".")
            )
        return paths

    def _parse_dictionary(self, relative_path: Path) -> dict[str, Any]:
        keywords = (
            keyword for keyword in self._get_keywords(relative_path) if keyword != "FoamFile"
        )
        return {keyword: self._parse_entry(relative_path, keyword) for keyword in keywords}

    def _parse_entry(self, relative_path: Path, entry: str) -> Any:
        try:
            child_keywords = self._get_keywords(relative_path, entry=entry)
        except CommandExecutionError:
            child_keywords = []
        if child_keywords:
            return {
                child: self._parse_entry(relative_path, f"{entry}/{child}")
                for child in child_keywords
            }
        return self._get_value(relative_path, entry)

    def _get_keywords(self, relative_path: Path, *, entry: str | None = None) -> list[str]:
        command = ["foamDictionary"]
        if entry is not None:
            command.extend(("-entry", entry))
        command.extend(("-keywords", str(relative_path)))
        output = self._execute(command)
        return self._parse_keywords(output)

    def _get_value(self, relative_path: Path, entry: str) -> Any:
        output = self._execute(["foamDictionary", "-entry", entry, "-value", str(relative_path)])
        return self._parse_value(output)

    def _execute(self, command: list[str]) -> str:
        result = self._run_command(command, self.case_path, capture_output=True)
        return result.stdout or ""

    @staticmethod
    def _parse_keywords(output: str) -> list[str]:
        text = output.strip()
        if text.startswith("(") and text.endswith(")"):
            text = text[1:-1].strip()
        lines = [line.strip().rstrip(";") for line in text.splitlines()]
        lines = [line for line in lines if line and line not in {"(", ")", "{", "}"}]
        if len(lines) == 1:
            return shlex.split(lines[0])
        return [line.strip('"') for line in lines]

    @staticmethod
    def _parse_value(output: str) -> Any:
        value = output.strip().rstrip(";").strip()
        if value in {"true", "false"}:
            return value == "true"
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if len(value) >= 2 and value[0] == value[-1] == '"':
            return value[1:-1]
        return value
