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
    newPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePath, dist_path=newPath, mode='rewrite')


    sc = SetSystem(pathCase=newPath)
    sc.setControlDict(controlDict)


    meshClass = Mesh(pathCase=newPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()


    ic = InitialValue(pathCase=newPath)
    newDict= ic.calcInitVal(A, B, Uin, nu)
    ic.setVarAllFiles(constDictVar, newDict)


    cc = SetConstantParam(pathCase=newPath)
    cc.set_transportProp(tranPropDict)
    cc.setTurbModel(typeTurbModel='kEpsilon')


    rc = Runner()
    rc.setCores()
    rc.setPathCase(newPath)
    rc.set_solver_name()
    rc.set_mode(mode='common')
    rc.set_pyFoam_settings(pyFoam=False)
    rc.runCase()
