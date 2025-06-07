from pyRunOF.modules.constant import Constant
from pyRunOF.modules.elmer import Elmer
from pyRunOF.modules.initial_values import InitialValues
from pyRunOF.modules.meshes import Mesh
from pyRunOF.modules.model_config import ModelConfigurator
from pyRunOF.modules.parametric_sweep import ParametricSweep
from pyRunOF.modules.post_process import PostProcess
from pyRunOF.modules.run import Run
from pyRunOF.modules.set_system import System

VERSION = "0.1.0"
__version__ = VERSION

#TODO: here I test new import 
def __getattr__(attr):
    if attr == "constant":
            print('HI!')
            import pyRunOF.modules.constant as const
            from pyRunOF.modules.constant import Constant
            return const
    elif attr == "elmer":
        from pyRunOF.modules.elmer import Elmer
        return Elmer
    else:
         raise AttributeError("module {!r} has no attribute "
                             "{!r}".format(__name__, attr))

