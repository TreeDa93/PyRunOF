import importlib.util
import json
from pathlib import Path

from pyRunOF.openfoam import CaseParser, CaseSchemaArtifacts


def _parsed_case() -> dict:
    return {
        "schema_version": 1,
        "case": {"name": "base-case"},
        "constant": {"transportProperties": {"nu": 1e-5}},
        "system": {
            "controlDict": {
                "application": "icoFoam",
                "endTime": 100,
                "adjustTimeStep": True,
            }
        },
    }


def test_export_schema_creates_config_schema_and_importable_types(
    tmp_path: Path, monkeypatch
) -> None:
    parser = CaseParser(tmp_path)
    monkeypatch.setattr(parser, "parse", lambda **_options: _parsed_case())

    artifacts = parser.export_schema(
        tmp_path / "generated/base_case", name="BaseCase", progress=False
    )

    assert isinstance(artifacts, CaseSchemaArtifacts)
    assert artifacts.directory == tmp_path / "generated/base_case"
    assert {path.name for path in (artifacts.config, artifacts.schema, artifacts.types)} == {
        "config.json",
        "schema.json",
        "types.py",
    }
    assert all(path.is_file() for path in (artifacts.config, artifacts.schema, artifacts.types))

    config = json.loads(artifacts.config.read_text(encoding="utf-8"))
    assert config["system"]["controlDict"]["endTime"] == 100
    assert "generated_at" in config

    schema = json.loads(artifacts.schema.read_text(encoding="utf-8"))
    control = schema["properties"]["system"]["properties"]["controlDict"]
    assert control["properties"]["endTime"] == {"type": "integer"}
    assert control["properties"]["adjustTimeStep"] == {"type": "boolean"}
    assert control["additionalProperties"] is True

    spec = importlib.util.spec_from_file_location("generated_case_types", artifacts.types)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.CaseSettings is module.BaseCaseSettings
    assert "system" in module.CaseSettings.__annotations__


def test_generated_types_preserve_non_identifier_openfoam_keys(
    tmp_path: Path, monkeypatch
) -> None:
    parser = CaseParser(tmp_path)
    data = {"system": {"fvSchemes": {"div(phi,U)": "Gauss upwind"}}}
    monkeypatch.setattr(parser, "parse", lambda **_options: data)

    artifacts = parser.export_schema(tmp_path / "generated", progress=False)
    source = artifacts.types.read_text(encoding="utf-8")

    assert '"div(phi,U)": str' in source
