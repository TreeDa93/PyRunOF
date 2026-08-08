from pathlib import Path

import pytest

from pyRunOF import ModelConfigurator, UnsafePathError


@pytest.fixture
def configurator(tmp_path: Path) -> ModelConfigurator:
    return ModelConfigurator(
        dir_path=tmp_path,
        info={
            "general": {
                "paths": {"dir": tmp_path},
                "case_names": {},
            }
        },
    )


def test_create_folder_does_not_overwrite_by_default(
    configurator: ModelConfigurator, tmp_path: Path
) -> None:
    target = tmp_path / "case"
    target.mkdir()
    marker = target / "result.dat"
    marker.write_text("important", encoding="utf-8")

    with pytest.raises(FileExistsError):
        configurator.create_folder(directory=tmp_path, folder_name="case")

    assert marker.read_text(encoding="utf-8") == "important"


def test_create_folder_can_explicitly_replace(
    configurator: ModelConfigurator, tmp_path: Path
) -> None:
    target = tmp_path / "case"
    target.mkdir()
    (target / "old").write_text("old", encoding="utf-8")

    configurator.create_folder(directory=tmp_path, folder_name="case", rewrite=True)

    assert target.is_dir()
    assert list(target.iterdir()) == []


def test_delete_rejects_path_outside_case_root(
    configurator: ModelConfigurator, tmp_path: Path
) -> None:
    outside = tmp_path.parent / "must-not-be-deleted"
    outside.mkdir(exist_ok=True)
    try:
        with pytest.raises(UnsafePathError):
            configurator.delete_folders([outside], directory=tmp_path)
        assert outside.exists()
    finally:
        outside.rmdir()


def test_find_folders_by_word_only_returns_directories(
    configurator: ModelConfigurator, tmp_path: Path
) -> None:
    match = tmp_path / "case_alpha"
    match.mkdir()
    (tmp_path / "case_file").write_text("not a directory", encoding="utf-8")

    paths, names = configurator.find_folders_by_word("case", directory=tmp_path)

    assert paths == [match]
    assert names == ["case_alpha"]


def test_duplicate_rewrite_replaces_destination(
    configurator: ModelConfigurator, tmp_path: Path
) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()
    (source / "controlDict").write_text("new", encoding="utf-8")
    (destination / "old").write_text("old", encoding="utf-8")

    configurator.duplicate_case(source, destination, mode="rewrite")

    assert (destination / "controlDict").read_text(encoding="utf-8") == "new"
    assert not (destination / "old").exists()
