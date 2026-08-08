"""Case configuration and filesystem operations."""

from pyRunOF.case.config import CaseConfig

__all__ = ["CaseConfig", "ModelConfigurator"]


def __getattr__(name):
    if name == "ModelConfigurator":
        from pyRunOF.modules.model_config import ModelConfigurator

        return ModelConfigurator
    raise AttributeError(name)
