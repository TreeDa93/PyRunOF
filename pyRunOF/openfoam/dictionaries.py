"""OpenFOAM dictionary configuration."""

from pyRunOF.additional_fun.foam_dictionaries import (
    add_foamDict_items,
    get_solution_time,
    print_content,
    print_dict_value,
    print_foamDict_keys,
    print_sub_content,
    set_foamDict_value,
)
from pyRunOF.modules.constant import Constant
from pyRunOF.modules.set_system import System

__all__ = [
    "Constant",
    "System",
    "add_foamDict_items",
    "get_solution_time",
    "print_content",
    "print_dict_value",
    "print_foamDict_keys",
    "print_sub_content",
    "set_foamDict_value",
]
