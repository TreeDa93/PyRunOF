"""Generate JSON Schema and Python typing artifacts from parsed case data."""

from __future__ import annotations

import json
import keyword
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class CaseSchemaArtifacts:
    """Paths created by :meth:`CaseParser.export_schema`."""

    directory: Path
    config: Path
    schema: Path
    types: Path


def normalize_type_name(name: str) -> str:
    """Return a valid public Python class name."""
    words = re.findall(r"[A-Za-z0-9]+", name)
    result = "".join(word[:1].upper() + word[1:] for word in words) or "OpenFOAMCase"
    if result[0].isdigit():
        result = f"Case{result}"
    if keyword.iskeyword(result):
        result += "Case"
    return result


def build_json_schema(data: Any, *, title: str) -> dict[str, Any]:
    """Build a permissive JSON Schema that documents all observed values."""
    schema = _schema_for(data)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:pyrunof:{title}",
        "title": title,
        **schema,
    }


def _schema_for(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            "type": "object",
            "properties": {str(key): _schema_for(item) for key, item in value.items()},
            # OpenFOAM dictionaries are extensible, so generated schemas suggest
            # known entries without rejecting custom solver entries.
            "additionalProperties": True,
        }
    if isinstance(value, list):
        item_schemas = _unique_dicts(_schema_for(item) for item in value)
        if not item_schemas:
            items: dict[str, Any] = {}
        elif len(item_schemas) == 1:
            items = item_schemas[0]
        else:
            items = {"anyOf": item_schemas}
        return {"type": "array", "items": items}
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    return {"type": "string"}


def _unique_dicts(values: Any) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return unique


class _TypedDictGenerator:
    def __init__(self, root_name: str):
        self.root_name = root_name
        self.definitions: list[tuple[str, list[tuple[str, str]]]] = []
        self.used_names: set[str] = set()

    def render(self, data: dict[str, Any]) -> str:
        root = self._mapping_type(data, (self.root_name,))
        blocks = [
            '"""Generated types for a parsed OpenFOAM case. Do not edit manually."""',
            "",
            "from __future__ import annotations",
            "",
            "from typing import Any, TypedDict",
            "",
        ]
        for class_name, fields in self.definitions:
            rendered_fields = ",\n".join(
                f"        {json.dumps(key, ensure_ascii=False)}: {annotation}"
                for key, annotation in fields
            )
            blocks.extend(
                [
                    f"{class_name} = TypedDict(",
                    f"    {class_name!r},",
                    "    {",
                    rendered_fields,
                    "    },",
                    "    total=False,",
                    ")",
                    "",
                ]
            )
        blocks.extend([f"CaseSettings = {root}", "", '__all__ = ["CaseSettings"]', ""])
        return "\n".join(blocks)

    def _mapping_type(self, value: dict[str, Any], path: tuple[str, ...]) -> str:
        base_name = normalize_type_name(" ".join(path))
        class_name = base_name
        suffix = 2
        while class_name in self.used_names:
            class_name = f"{base_name}{suffix}"
            suffix += 1
        self.used_names.add(class_name)
        fields = [(str(key), self._type_for(item, (*path, str(key)))) for key, item in value.items()]
        # Children are registered first, so their names exist before this definition.
        self.definitions.append((class_name, fields))
        return class_name

    def _type_for(self, value: Any, path: tuple[str, ...]) -> str:
        if isinstance(value, dict):
            return self._mapping_type(value, path)
        if isinstance(value, list):
            annotations = list(dict.fromkeys(self._type_for(item, (*path, "Item")) for item in value))
            return f"list[{' | '.join(annotations) if annotations else 'Any'}]"
        if value is None:
            return "None"
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "str"
        return "Any"


def generate_typed_dicts(data: dict[str, Any], *, name: str) -> str:
    """Return an importable module containing nested ``TypedDict`` definitions."""
    root_name = f"{normalize_type_name(name)}Settings"
    return _TypedDictGenerator(root_name).render(data)


__all__ = [
    "CaseSchemaArtifacts",
    "build_json_schema",
    "generate_typed_dicts",
    "normalize_type_name",
]
