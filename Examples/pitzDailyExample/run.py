import os, sys
libpath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(libpath)


from Modules.Manipulations import Manipulations
from Modules.RunApplication import Runner
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import IntiailValue
from Modules.setConstant import SetConstantParam



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


    ic = IntiailValue(pathCase=runPath)
    ic.setVarAllFiels(constDictVar)

    cc = SetConstantParam(pathCase=runPath)
    cc.setTransportProp(tranPropDict)



    rc = Runner()
    rc.setCores()
    rc.setPathCase(runPath)
    rc.setNameSolver(solverName=solverName)
    rc.setModeRunner(mode='common')
    rc.setPyFoamSettings(pyFoam=False)
    rc.runCase()
