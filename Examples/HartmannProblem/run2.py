import sys # import library
libpath = '/home/ivan/mySolvers/pyFoamRun/' #write path to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes

from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.Manipulations import Manipulations
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import InitialValue
from Modules.setConstant import SetConstantParam
from Modules.RunApplication import Runner
from Modules.Elmer import Elmer

def main():



    #step2(step1())
    oldpath = 'step1_solved'
    #hartmann(step1())
    hartmann(oldpath)






def step1():
    generalPath= os.getcwd()
    mc = Manipulations(basePath=basePathStep1)
    mc.generatorNewName(prefixName, baseNewName=baseName1) #return name
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    runPath = mc.getPath('newPath')
    mc.dublicateCase(basePath=basePathStep1, newPath=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    initialClass = InitialValue(pathCase=runPath)
    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    meshClass = Mesh(pathCase=runPath)


    sc.setControlDict(controlDict)

    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiles(initialDictConst, initialDictCalculated)

    cpClass.setTurbModel2(turbType1)
    cpClass.setTransportProp(tranPropDict)


    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(pathCase=runPath)
    rc.setCoresOF(coreOF=coreOFstep1)
    rc.setNameSolver(solverName=solverName1)
    rc.setModeRunner(mode=modeStep1)
    rc.setPyFoamSettings(pyFoam=False)
    rc.setDecomposeParDict(nameVar=nameCoreOF)
    rc.runCase()

    os.chdir(generalPath)
    return os.path.abspath(runPath)


def hartmann(oldPath):
    generalPath = os.getcwd()
    mc = Manipulations(basePath=basePathStep2) # initialize manipulation class
    mc.generatorNewName(prefixName2, baseNewName=baseName2)
    newName = mc.getName('newName')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=newName, keyPath='newPath')
    mc.createNewPath(dirmame=os.getcwd(), newCaseName=oldPath, keyPath='oldPath')
    runPath = mc.getPath('newPath')
    oldPath = mc.getPath('oldPath')
    mc.dublicateCase(basePath=basePathStep2, newPath=runPath, mode=modeManipul2)

    # initialization all required classes
    sc = SetSystem(pathCase=runPath)
    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    initialClass = InitialValue(pathCase=runPath)
    meshClass = Mesh(pathCase=runPath)
    eClass = Elmer(pathCase=runPath, sifName='case.sif')
    rc = Runner(pathCase=runPath)


    sc.setControlDict(controlDict) # настраиваем controlDict
    cpClass.setTurbModel2(turbType1)  # настраиваем модель турбулентности
    cpClass.setTransportProp(tranPropDict)  # настраиваем transportProperties in constant

    meshClass.setBlockMesh(meshList)   # настраиваем BlockMeshDict
    meshClass.runBlockMesh()             # запускаем BlockMesh
    meshClass.settingsElmerMesh(elmerMeshDict, pathCase=None, elmerMeshName='Elmer_EOF')
    meshClass.runElmerMesh()

    # устанавиваем настрйоки источника и назначение кейсов
    initialClass.setMappSettings(sourcePath=oldPath, distPath=runPath, source='0.25', dist='0')
    # задаем значения для tVMFV
    initialClass.settingsTimeVaryingMappedFixedValue(nameSample='outletSurf',
                                                     sourceTimeStep =0.25, namePatch='outlet')
    initialClass.setTimeVaryingMappedFixedValue()       # устанавливаем значения для BC tVMFV

    eClass.setElmerVar(elmerDict) # Устанавливаем значения в sif файле

    rc.setCoresEOF(coreOF=coreOF2, coreElmer=coreElmer2, elmerMeshName=meshClass.elmerMeshName) # set core for Eler and OF
    rc.setNameSolver(solverName=solverName)    # set name of solver
    rc.setModeRunner(mode=mode2)                 # set mode to run
    rc.setPyFoamSettings(pyFoam=False)          # set to run pyFoam
    rc.setDecomposeParDict(nameVar=varcoreOF)       # write core to decomposeParDict

    # write settings for mapFields
    initialClass.settingsMapField(consistent=True, mapMethod='mapNearest', parallelSource=True,
                         parallelTarget=False, sourceTime=0.25)
    # create command mapFields
    initialClass.createMapFieldCommand()
    # run mapFields
    initialClass.mapFieldsRun(check=True)

    rc.decompose(True)
    rc.decomposeElmer(True)

    rc.runCase()   # run case
    os.chdir(generalPath)
    return os.path.abspath(runPath)


if __name__ == "__main__":
    main()