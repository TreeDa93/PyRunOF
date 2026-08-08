from pathlib import Path

from pyRunOF import CaseConfig, Elmer, OpenFOAMCase
from pyRunOF.case import ModelConfigurator
from pyRunOF.openfoam import Run
from pyRunOF.openfoam.dictionaries import Constant, System


def test_case_config_normalizes_paths(tmp_path: Path) -> None:
    config = CaseConfig.from_mapping(
        "channel",
        {
            "case_path": tmp_path,
            "paths": {"results": tmp_path / "results"},
            "case_names": {"solver": "pimpleFoam"},
            "cores": 8,
        },
    )

    assert config.path() == tmp_path
    assert config.path("results") == tmp_path / "results"
    assert config.name("solver") == "pimpleFoam"
    assert config.parameters["cores"] == 8


def test_components_accept_shared_case_config(tmp_path: Path) -> None:
    config = CaseConfig(key="channel", case_path=tmp_path)

    runner = Run(config=config, solver="icoFoam")
    constant = Constant(config=config)
    system = System(config=config)

    assert runner.config.case_path == tmp_path
    assert constant.get_constant_path() == tmp_path / "constant"
    assert system.get_system_path() == tmp_path / "system"


def test_openfoam_case_groups_components(tmp_path: Path) -> None:
    case = OpenFOAMCase(tmp_path)

    assert case.path == tmp_path
    assert case.runner.config.case_path == tmp_path
    assert case.mesh.config.case_path == tmp_path


def test_elmer_can_be_initialized(tmp_path: Path) -> None:
    elmer = Elmer(case_path=tmp_path, sif_name="solver")

    assert elmer.config.case_path == tmp_path
    assert elmer.info["general"]["name"] == "solver"


def test_case_package_exposes_model_configurator() -> None:
    assert ModelConfigurator.__name__ == "ModelConfigurator"
