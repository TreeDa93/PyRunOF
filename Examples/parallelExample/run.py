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
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePath, newPath=runPath, mode='rewrite')


    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)


    Mesh().runBlockMesh(pathCase=runPath)


    ic = InitialValue(pathCase=runPath)
    ic.setVarAllFiles(constDictVar)

    cc = SetConstantParam(pathCase=runPath)
    cc.set_transportProp(tranPropDict)   # write viscosity in transportProperies



    rc = Runner()
    rc.setPathCase(runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.setNameSolver(solverName=solverName)
    rc.setModeRunner(mode='parallel')
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()
