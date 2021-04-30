import sys # import library
libpath = '/home/ivan/mySolvers/pyFoamRun/' #write path to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes
/home/ivan/mySolvers/pyFoamRun/step1_solved
from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.Manipulations import Manipulations
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import IntiailValue
from Modules.setConstant import SetConstantParam
from Modules.RunApplication import Runner

def main():




    #step2(step1())
    oldpath = 'step1_solved'
    step2(oldpath)






def step1():
    generalPath= os.getcwd()
    mc = Manipulations(basePath=basePathStep1)
    mc.generatorNewName(prefixName, baseNewName=baseName1) #return name
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePathStep1, newPath=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiels(initialDictConst, initialDictCalculated)

    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    cpClass.setTurbModel2(turbType1)
    cpClass.setTransportProp(tranPropDict)

    meshClass = Mesh(pathCase=runPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(pathCase=runPath)
    rc.setCoresOF(coreOF=coreOFstep1)
    rc.setNameSolver(solverName=solverName1)
    rc.setModeRunner(mode=modeStep1)
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar=nameCoreOF)
    rc.runCase()

    os.chdir(generalPath)
    return os.path.abspath(runPath)



def step2(oldPath):
    generalPath = os.getcwd()
    mc = Manipulations(basePath=basePathStep2)
    mc.generatorNewName(prefixName2, baseNewName=baseName2)
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName, keyPath='newPath')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=oldPath, keyPath='oldPath')
    runPath = mc.getPath('newPath')
    oldPath = mc.getPath('oldPath')
    mc.dublicateCase(basePath=basePathStep2, newPath=runPath, mode=modeManipul2)

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialClass.setMappSettings(sourcePath=oldPath, distPath=runPath, source='0.25', dist='0')
    initialClass.copyBC(nameBCsource='outlet', nameBCdist='inlet',
                                mapTimeStep=stopTime)
    initialClass.reconstruct(oldPath)
    initialClass.setMappValues()

    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    cpClass.setTurbModel2(turbType1)
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



def developedFlow():
    step3(step2(step1()))

if __name__ == "__main__":
    main()