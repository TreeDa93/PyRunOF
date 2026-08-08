import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from pyRunOF import CaseParser, OpenFOAMCase
from pyRunOF.exceptions import CommandExecutionError, UnsafePathError


class FakeFoamDictionary:
    def __init__(self):
        self.calls: list[list[str]] = []
        self.keywords = {
            ("0/U", None): ["dimensions", "internalField", "boundaryField"],
            ("0/U", "boundaryField"): ["inlet", "outlet", "walls"],
            ("0/U", "boundaryField/inlet"): ["type", "value"],
            ("0/U", "boundaryField/outlet"): ["type"],
            ("0/U", "boundaryField/walls"): ["type"],
            ("constant/transportProperties", None): ["transportModel", "nu"],
            ("system/controlDict", None): ["application", "endTime", "writeInterval"],
            ("system/fvSchemes", None): ["ddtSchemes"],
            ("system/fvSchemes", "ddtSchemes"): ["default"],
        }
        self.values = {
            ("0/U", "dimensions"): "[0 1 -1 0 0 0 0]",
            ("0/U", "internalField"): "uniform (0 0 0)",
            ("0/U", "boundaryField/inlet/type"): "fixedValue",
            ("0/U", "boundaryField/inlet/value"): "uniform (1 0 0)",
            ("0/U", "boundaryField/outlet/type"): "zeroGradient",
            ("0/U", "boundaryField/walls/type"): "noSlip",
            ("constant/transportProperties", "transportModel"): "Newtonian",
            ("constant/transportProperties", "nu"): "1e-05",
            ("system/controlDict", "application"): "icoFoam",
            ("system/controlDict", "endTime"): "100",
            ("system/controlDict", "writeInterval"): "10",
            ("system/fvSchemes", "ddtSchemes/default"): "Euler",
        }

    def __call__(self, command, case_path, *, capture_output=False):
        assert capture_output is True
        self.calls.append(command)
        file_name = command[-1]
        entry = command[command.index("-entry") + 1] if "-entry" in command else None
        if "-set" in command:
            output = ""
        elif "-keywords" in command:
            try:
                output = "\n".join(self.keywords[(file_name, entry)])
            except KeyError as exc:
                raise CommandExecutionError("entry is not a dictionary") from exc
        else:
            output = self.values[(file_name, entry)]
        return SimpleNamespace(stdout=output)


def _create_case(root: Path) -> None:
    for relative in (
        "0/U",
        "constant/transportProperties",
        "constant/polyMesh/owner",
        "system/controlDict",
        "system/fvSchemes",
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("FoamFile {}", encoding="utf-8")


def test_parser_exports_fields_boundaries_and_case_dictionaries(tmp_path: Path) -> None:
    _create_case(tmp_path)
    fake = FakeFoamDictionary()

    result = CaseParser(tmp_path, command_runner=fake).parse()

    velocity = result["initial_conditions"]["U"]
    assert velocity["internalField"] == "uniform (0 0 0)"
    assert velocity["boundaryField"] == {
        "inlet": {"type": "fixedValue", "value": "uniform (1 0 0)"},
        "outlet": {"type": "zeroGradient"},
        "walls": {"type": "noSlip"},
    }
    assert result["constant"]["transportProperties"]["nu"] == 1e-5
    assert result["system"]["controlDict"]["application"] == "icoFoam"
    assert result["system"]["fvSchemes"]["ddtSchemes"] == {"default": "Euler"}
    assert "owner" not in result["constant"]
    assert all("constant/polyMesh" not in call for call in fake.calls)


def test_parser_saves_single_json_file(tmp_path: Path) -> None:
    _create_case(tmp_path)
    destination = CaseParser(tmp_path, command_runner=FakeFoamDictionary()).save("settings.json")

    data = json.loads(destination.read_text(encoding="utf-8"))
    assert destination == tmp_path / "settings.json"
    assert data["schema_version"] == 1
    assert data["case"]["name"] == tmp_path.name
    assert "generated_at" in data


def test_openfoam_case_exposes_parser(tmp_path: Path) -> None:
    assert isinstance(OpenFOAMCase(tmp_path).parser, CaseParser)


def test_parser_applies_initial_boundary_constant_and_system_values(tmp_path: Path) -> None:
    _create_case(tmp_path)
    fake = FakeFoamDictionary()
    settings = {
        "initial_conditions": {
            "U": {
                "internalField": "uniform (0.5 0 0)",
                "boundaryField": {
                    "inlet": {"type": "fixedValue", "value": "uniform (2 0 0)"}
                },
            }
        },
        "constant": {"transportProperties": {"nu": 2e-5}},
        "system": {"controlDict": {"endTime": 250, "writeInterval": 25}},
    }

    report = CaseParser(tmp_path, command_runner=fake).apply(settings)

    assert report == {"updated": 6, "errors": []}
    set_calls = [call for call in fake.calls if "-set" in call]
    assert [
        "foamDictionary",
        "-entry",
        "boundaryField/inlet/value",
        "-set",
        "uniform (2 0 0)",
        "0/U",
    ] in set_calls
    assert [
        "foamDictionary",
        "-entry",
        "nu",
        "-set",
        "2e-05",
        "constant/transportProperties",
    ] in set_calls
    assert [
        "foamDictionary",
        "-entry",
        "endTime",
        "-set",
        "250",
        "system/controlDict",
    ] in set_calls


def test_parser_applies_settings_from_json(tmp_path: Path) -> None:
    _create_case(tmp_path)
    settings_path = tmp_path / "changes.json"
    settings_path.write_text(
        json.dumps({"system": {"controlDict": {"endTime": 500}}}), encoding="utf-8"
    )
    fake = FakeFoamDictionary()

    report = CaseParser(tmp_path, command_runner=fake).apply(settings_path)

    assert report["updated"] == 1
    assert fake.calls[-1][-2:] == ["500", "system/controlDict"]


def test_parser_refuses_to_modify_polymesh(tmp_path: Path) -> None:
    _create_case(tmp_path)
    parser = CaseParser(tmp_path, command_runner=FakeFoamDictionary())

    with pytest.raises(UnsafePathError, match="polyMesh"):
        parser.apply({"constant": {"polyMesh/owner": {"value": 1}}})
