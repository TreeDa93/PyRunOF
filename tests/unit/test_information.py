from pathlib import Path

import pytest

from pyRunOF import ModelConfigurator


def test_information_dictionary_is_merged(tmp_path: Path) -> None:
    configurator = ModelConfigurator(
        info={"general": {"paths": {"case": tmp_path}, "case_names": {"run": "a"}}}
    )
    assert configurator.get_path("case") == tmp_path
    assert configurator.get_name("run") == "a"


def test_information_rejects_wrong_type() -> None:
    with pytest.raises(TypeError, match="dictionary"):
        ModelConfigurator(info=[])
