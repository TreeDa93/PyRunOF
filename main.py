import os
from Modules.Manipulations import Manipulations
from Modules.RunApplication import Runner
from Modules.Meshes import Mesh

testPath = os.path.abspath('newTest')
basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/icoFoam/cavity/cavity'
dictionary = {'newPath': testPath,
              'numCoreOF': 4,
              'numCoreEOF': 4,
              'solverName': 'icoFoam',
              'mode': 'common'}

if __name__ == "__main__":

    manipulationClass = Manipulations()
    manipulationClass.generatorNewNameFolder(1, 2, 3, baseNewCase='test')
    manipulationClass.createNewPath(dirmame=os.getcwd(), newCaseName=manipulationClass.newNameCase)
    manipulationClass.dublicateCase(baseCasePath=basePath, newPath=manipulationClass.newPath, mode='copy')
    meshClass = Mesh()
    meshClass.createOFMesh(manipulationClass.newPath)
    runClass = Runner()
    runClass.setCores()
    runClass.setNewPathCase(manipulationClass.newPath)
    runClass.setNameSolver(solverName='icoFoam')
    runClass.setModeRunner(mode='common')
    runClass.setPyFoamSettings(pyFoam=False)
    runClass.runCase()


