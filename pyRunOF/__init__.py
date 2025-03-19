from .modules.constant import Constant
from .modules.set_system import System
from .modules.elmer import Elmer
from .modules.initial_values import InitialValues
from .modules.manipulations import Manipulations
from .modules.meshes import Mesh
from .modules.parametric_sweep import ParametricSweep
from .modules.post_process import PostProcess
from .modules.run import Run
# ONLY FOR TEST!!!
from .modules._test_module import test_fun

VERSION = '0.1.0'
__version__ = VERSION