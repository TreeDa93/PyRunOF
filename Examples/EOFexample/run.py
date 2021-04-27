import os, sys
libpath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(libpath)

from Modules.Manipulations import Manipulations
from Modules.RunApplication import Runner

basePath = '2D_TMFHartmann'


if __name__ == "__main__":

    mc = Manipulations(basePath=basePath)
    mc.generatorNewName('solved', baseNewName=basePath)
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    newPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePath, newPath=newPath, mode='rewrite')


    rc = Runner()
    rc.setCores(numCoreOF=4, numCoreElmer=4)
    rc.setPathCase(newPath)
    rc.setNameSolver(solverName='mhdVxBPhasePimpleFoam')
    rc.setModeRunner(mode='EOF')
    rc.setPyFoamSettings(pyFoam=False)
    rc.runCase(decompose=True)
