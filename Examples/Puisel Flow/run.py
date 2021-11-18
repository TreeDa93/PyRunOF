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

    mc = Manipulations(basePath=basePath)
    mc.generatorNewName('solved', baseNewName=basePath)
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    newPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePath, newPath=newPath, mode='rewrite')


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
    rc.setNameSolver(solverName='pimpleFoam')
    rc.setModeRunner(mode='common')
    rc.setPyFoamSettings(pyFoam=False)
    rc.runCase()
