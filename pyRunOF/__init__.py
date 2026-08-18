"""PyRunOF public API."""

from pyRunOF.exceptions import (
    CommandExecutionError,
    ConfigurationError,
    PyRunOFError,
    UnsafePathError,
)
from pyRunOF.case.config import CaseConfig
from pyRunOF.openfoam.case import OpenFOAMCase
from pyRunOF.openfoam.parser import CaseParser
from pyRunOF.modules.constant import Constant
from pyRunOF.modules.elmer import Elmer
from pyRunOF.modules.initial_values import InitialValues
from pyRunOF.modules.meshes import Mesh
from pyRunOF.modules.model_config import ModelConfigurator
from pyRunOF.sweep import ParametricSweep, SweepExecutionError, SweepPoint
from pyRunOF.modules.post_process import PostProcess
from pyRunOF.modules.run import Run
from pyRunOF.modules.set_system import System

__version__ = "0.2.0"

__all__ = [
    "CommandExecutionError",
    "CaseConfig",
    "CaseParser",
    "ConfigurationError",
    "Constant",
    "Elmer",
    "InitialValues",
    "Mesh",
    "ModelConfigurator",
    "OpenFOAMCase",
    "ParametricSweep",
    "SweepExecutionError",
    "SweepPoint",
    "PostProcess",
    "PyRunOFError",
    "Run",
    "System",
    "UnsafePathError",
]
