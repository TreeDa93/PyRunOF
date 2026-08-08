from pathlib import Path

from pyRunOF.additional_fun import files
from pyRunOF.additional_fun.auxiliary_functions import Files, Priority
from pyRunOF.additional_fun import foam_dictionaries
from pyRunOF.modules.initial_values import InitialValues


def test_files_compatibility_class_uses_canonical_functions(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("old", encoding="utf-8")

    Files.change_var_fun("old", "new", tmp_path, source.name)

    assert source.read_text(encoding="utf-8") == "new"
    assert Files.open_json is files.open_json


def test_priority_compatibility_class_uses_priority_module():
    assert Priority.variable(None, {"cores": 4}, "cores") == 4
    assert Priority.path(None, {"case": "/tmp"}, "case") == Path("/tmp")
    assert Priority.name(None, {"solver": "pimpleFoam"}, "solver") == "pimpleFoam"


def test_foam_dictionary_builds_argument_list(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(
        foam_dictionaries,
        "run_command",
        lambda command, case_path: calls.append((command, case_path)),
    )

    foam_dictionaries.set_foamDict_value(
        {"startFrom": "startTime", "startTime": 0}, tmp_path, "system/controlDict"
    )

    assert calls == [
        (
            [
                "foamDictionary",
                "-set",
                "startFrom=startTime, startTime=0",
                "system/controlDict",
            ],
            tmp_path,
        )
    ]


def test_map_fields_command_has_explicit_argument_boundaries():
    initial_values = object.__new__(InitialValues)
    command = initial_values.createMapFieldCommand(
        {"-consistent": True, "-sourceTime": "latestTime", "src": "../source case"}
    )

    assert command == "mapFields -consistent -sourceTime latestTime '../source case'"
    assert initial_values._commandMapFields_args == [
        "mapFields", "-consistent", "-sourceTime", "latestTime", "../source case"
    ]
