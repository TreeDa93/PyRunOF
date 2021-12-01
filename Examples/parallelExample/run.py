import os, sys
libpath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(libpath)

from Modules.manipulations import Manipulations
from Modules.run import Runner
from Modules.meshes import Mesh
from Modules.set_system import System
from Modules.initial_value import InitialValue
from Modules.constant import Constant


from data import *


if __name__ == "__main__":

    mc = Manipulations(base_path=basePath)
    mc.create_name('solved', name_base=basePath)
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName)
    runPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePath, dist_path=runPath, mode='rewrite')


    sc = System()
    sc.setControlDict(controlDict)


    Mesh().run_blockMesh(case_path=runPath)


    ic = InitialValue(pathCase=runPath)
    ic.setVarAllFiles(constDictVar)

    cc = Constant(pathCase=runPath)
    cc.set_transportProp(tranPropDict)   # write viscosity in transportProperies



    rc = Runner()
    rc.setPathCase(runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.set_solver_name()
    rc.set_mode(mode='parallel')
    rc.set_pyFoam_settings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()
