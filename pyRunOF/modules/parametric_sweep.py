"""Backward-compatible imports for parametric studies.

New code should import these objects from :mod:`pyRunOF.sweep`.
"""

from pyRunOF.sweep.parametric import ParametricSweep, SweepExecutionError, SweepPoint

__all__ = ["ParametricSweep", "SweepExecutionError", "SweepPoint"]
