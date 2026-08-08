"""High-level facade for operations on a single OpenFOAM case."""

from __future__ import annotations

from pathlib import Path

from pyRunOF.case.config import CaseConfig


class OpenFOAMCase:
    """Group PyRunOF components around one shared case configuration."""

    def __init__(self, path: str | Path, *, key: str = "general") -> None:
        from pyRunOF.modules.constant import Constant
        from pyRunOF.modules.initial_values import InitialValues
        from pyRunOF.modules.meshes import Mesh
        from pyRunOF.modules.run import Run
        from pyRunOF.modules.set_system import System
        from pyRunOF.openfoam.parser import CaseParser

        self.config = CaseConfig(key=key, case_path=Path(path))
        self.constant = Constant(config=self.config)
        self.initial_values = InitialValues(config=self.config)
        self.mesh = Mesh(config=self.config)
        self.parser = CaseParser(self.config.case_path)
        self.runner = Run(config=self.config)
        self.system = System(config=self.config)

    @property
    def path(self) -> Path:
        return self.config.path()
