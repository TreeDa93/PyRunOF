import os, sys
libpath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(libpath)


from Modules.manipulations import Manipulations
from Modules.run import Runner
from Modules.meshes import Mesh
from Modules.set_system import SetSystem
from Modules.initial_value import InitialValue
from Modules.constant import SetConstantParam



from data import *


if __name__ == "__main__":

    mc = Manipulations(base_path=basePath)
    mc.create_name('solved', name_base=basePath)
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName)
    runPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePath, dist_path=runPath, mode='rewrite')


    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)


    Mesh().runBlockMesh(pathCase=runPath)


    ic = InitialValue(pathCase=runPath)
    ic.setVarAllFiles(constDictVar)

    cc = SetConstantParam(pathCase=runPath)
    cc.set_transportProp(tranPropDict)



    rc = Runner()
    rc.setCores()
    rc.setPathCase(runPath)
    rc.set_solver_name()
    rc.set_mode(mode='common')
    rc.set_pyFoam_settings(pyFoam=False)
    rc.runCase()
