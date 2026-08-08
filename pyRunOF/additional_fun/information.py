"""Compatibility layer for configuration-aware PyRunOF components.

New code should use :class:`pyRunOF.case.CaseConfig`.  ``Information`` remains
as a transition base class for the historical component classes.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pyRunOF.case.config import CaseConfig
from pyRunOF.exceptions import ConfigurationError


class Information:
    """Store one or more consistently shaped :class:`CaseConfig` objects."""

    def __init__(
        self,
        info_key: str = "general",
        case_path: str | Path | None = None,
        *,
        config: CaseConfig | None = None,
        info: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> None:
        if config is not None and info is not None:
            raise ConfigurationError("config and info cannot be provided together")
        if config is not None:
            configs = {config.key: config}
            self.info_key = config.key
        elif info is not None:
            if not isinstance(info, Mapping):
                raise TypeError("info must be a dictionary or None")
            configs = {
                key: CaseConfig.from_mapping(key, values) for key, values in info.items()
            }
            self.info_key = info_key if info_key in configs else next(iter(configs), info_key)
        else:
            configs = {info_key: CaseConfig(key=info_key, case_path=case_path)}
            self.info_key = info_key
        self._configs = configs
        self.info = {key: value.to_mapping() for key, value in configs.items()}

    @property
    def config(self) -> CaseConfig:
        """Configuration selected by ``info_key``."""
        return self.get_config()

    def get_config(self, info_key: str | None = None) -> CaseConfig:
        key = self.get_key(info_key)
        # Rebuild from the compatibility mapping so direct legacy mutations
        # of ``info`` are visible to the typed API.
        config = CaseConfig.from_mapping(key, self.info[key])
        self._configs[key] = config
        return config

    def get_key(self, key: str | None) -> str:
        selected = self.info_key if key is None else key
        if selected not in self.info:
            raise KeyError(f"Unknown information key: {selected!r}")
        return selected

    def get_name(self, name_key: str, info_key: str | None = None) -> str:
        return self.get_config(info_key).name(name_key)

    def create_name(
        self,
        *case_names: str,
        name_base: str = "",
        name_key: str = "new_name",
        splitter: str = "_",
        only_base: bool = False,
        info_key: str | None = None,
    ) -> None:
        key = self.get_key(info_key)
        name = name_base if only_base else name_base + splitter + splitter.join(map(str, case_names))
        self.info[key]["case_names"][name_key] = name

    def create_path_from_dir(
        self,
        dir_path: str | Path | None = None,
        dir_path_key: str = "dir",
        folder_name: str | None = None,
        folder_name_key: str | None = None,
        path_key: str = "new",
        info_key: str | None = None,
        **legacy_options,
    ) -> Path:
        # ``name_key`` was used by older example scripts.
        folder_name_key = legacy_options.get("name_key", folder_name_key)
        config = self.get_config(info_key)
        directory = Path(dir_path) if dir_path is not None else config.path(dir_path_key)
        name = folder_name if folder_name is not None else config.name(folder_name_key)
        result = directory / name
        self.info[config.key]["paths"][path_key] = result
        return result

    def create_path(self, path, path_key: str = "default__path_key", info_key=None) -> None:
        self.info[self.get_key(info_key)]["paths"][path_key] = Path(path)

    def change_path(self, new_path: str | Path, path_key: str = "newPath") -> None:
        paths = self.info[self.info_key]["paths"]
        if path_key not in paths:
            raise KeyError(f"Unknown path key: {path_key!r}")
        paths[path_key] = Path(new_path)

    def get_path(self, path_key: str, info_key=None) -> Path:
        return self.get_config(info_key).path(path_key)

    def set_new_parameter(
        self, parameter: Any, info_key: str | None = None, parameter_name: str = "new_parameter"
    ) -> None:
        self.info[self.get_key(info_key)][parameter_name] = parameter

    def get_any_parameter(self, param_key: str, info_key: str | None = None) -> Any:
        return self.info[self.get_key(info_key)][param_key]

    def _case_path(self, case_path=None, info_key=None, path_key="case_path") -> Path:
        if case_path is not None:
            return Path(case_path)
        config = self.get_config(info_key)
        return config.path(path_key)

    def get_constant_path(self, case_path=None, info_key=None) -> Path:
        return self._case_path(case_path, info_key) / "constant"

    def get_system_path(self, case_path=None, info_key=None, path_key=None) -> Path:
        return self._case_path(case_path, info_key, path_key or "case_path") / "system"

    def get_any_folder_path(self, folder_name, case_path=None, info_key=None) -> Path:
        return self._case_path(case_path, info_key) / folder_name

    def find_all_sif(self, folder_path=None, info_key=None) -> list[Path]:
        path = self._case_path(folder_path, info_key)
        return list(path.glob("**/*.sif"))

    def find_all_zero_files(self, path_case=None, info_key=None) -> list[str]:
        return [path.stem for path in self.find_all_path_zero_files(path_case, info_key)]

    def find_all_path_zero_files(self, path_case=None, info_key=None) -> list[Path]:
        zero = self._case_path(path_case, info_key) / "0"
        return [path for path in zero.iterdir() if path.is_file()]

    def collect_information(self, *objects, key_info=None) -> None:
        for obj in objects:
            for key, values in obj.info.items():
                target = self.info.setdefault(
                    key, CaseConfig(key=key).to_mapping()
                )
                for name, value in values.items():
                    if isinstance(value, dict) and isinstance(target.get(name), dict):
                        target[name].update(value)
                    else:
                        target[name] = value

    def _initialize_component(self, **options) -> None:
        info_key = options.get("info_key", "general") or "general"
        config = options.get("config")
        info = options.get("info")
        Information.__init__(
            self, info_key, options.get("case_path"), config=config, info=info
        )

    def __init_manipulation__(self, **options):
        self._initialize_component(**options)
        key = self.info_key
        self.info[key]["paths"].setdefault("dir", self._check_type_path(options.get("dir_path")))
        self.info[key]["paths"].setdefault("cwd", Path.cwd())

    def __init_elmer__(self, **options):
        self._initialize_component(**options)
        self.info[self.info_key]["name"] = options.get("sif_name")

    def __init_constant__(self, **options):
        self._initialize_component(**options)

    def __init_iv__(self, **options):
        self._initialize_component(**options)

    def __init_mesh__(self, **options):
        self._initialize_component(**options)
        self.info[self.info_key]["elmer_mesh_name"] = options.get("e_mesh")

    def __init_system__(self, **options):
        self._initialize_component(**options)

    def __init_runner__(self, **options):
        self._initialize_component(**options)
        self.info[self.info_key].update(
            solver=options.get("solver", "pimpleFoam"),
            mode=options.get("mode", "common"),
            pyFoam=options.get("pyFoam", False),
            log=options.get("log", False),
            OF_core=options.get("OF_core", 2),
            E_core=options.get("E_core", 2),
        )

    @staticmethod
    def _check_type_path(path):
        return None if path is None else Path(path)

    @staticmethod
    def _check_prefix_sif(sif_name: str) -> str:
        return sif_name if sif_name.endswith(".sif") else f"{sif_name}.sif"
