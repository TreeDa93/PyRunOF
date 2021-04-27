import sys # import library
libpath = '/home/ivan/mySolvers/RunnerForCases/' #write path to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes

from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.Manipulations import Manipulations
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import IntiailValue
from Modules.setConstant import SetConstantParam
from Modules.RunApplication import Runner

def main():


    step3(step2(step1()))






def step1():
    generalPath= os.getcwd()
    mc = Manipulations(basePath=basePathStep1)
    mc.generatorNewName('parabolic', 'solved', baseNewName='step1')
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePathStep1, newPath=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiels(initialDictConst, initialDictCalculated)

    cpClass = SetConstantParam(pathCase=runPath)
    cpClass.setTurbModel(turbType)
    cpClass.setTransportProp(tranPropDict)

    meshClass = Mesh(pathCase=runPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(pathCase=runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.setNameSolver(solverName=solverName)
    rc.setModeRunner(mode=mode)
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()

    os.chdir(generalPath)
    return os.path.abspath(runPath)

def step2(oldpath):
    generalPath = os.getcwd()
    mc = Manipulations(basePath=basePathStep2)
    mc.generatorNewName('parabolic', 'solved', baseNewName='step2')
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePathStep2, newPath=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialClass.copyBC(oldpath, runPath, nameBCsource='outlet', nameBCdist='inlet',
                                mapTimeStep=stopTime)

    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiels(initialDictConst, initialDictCalculated)

    cpClass = SetConstantParam(pathCase=runPath)
    cpClass.setTurbModel(turbType)
    cpClass.setTransportProp(tranPropDict)

    meshClass = Mesh(pathCase=runPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(pathCase=runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.setNameSolver(solverName=solverName)
    rc.setModeRunner(mode=mode)
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()
    os.chdir(generalPath)
    return os.path.abspath(runPath)

def step3(oldpath):
    generalPath = os.getcwd()
    mc = Manipulations(basePath=basePathStep2)
    mc.generatorNewName('parabolic', 'solved', 'mapped', baseNewName='step2')
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePathStep2, newPath=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialClass.copyBC(oldpath, runPath, nameBCsource='outlet', nameBCdist='inlet',
                                mapTimeStep=stopTime)
    initialClass.setMappSet(sourcePath=oldpath, distPath=runPath, source='0', dist='0')
    initialClass.setMappValues()

    cpClass = SetConstantParam(pathCase=runPath)
    cpClass.setTurbModel(turbType)
    cpClass.setTransportProp(tranPropDict)

    meshClass = Mesh(pathCase=runPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(pathCase=runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.setNameSolver(solverName=solverName)
    rc.setModeRunner(mode=mode)
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()
    os.chdir(generalPath)
    return os.path.abspath(runPath)

if __name__ == "__main__":
    main()