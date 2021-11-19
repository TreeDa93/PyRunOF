import sys # import library
libpath = '/home/ivan/mySolvers/pyFoamRun/' #write name to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes

from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.manipulations import Manipulations
from Modules.meshes import Mesh
from Modules.set_system import SetSystem
from Modules.initial_value import IntiailValue
from Modules.constant import SetConstantParam
from Modules.run import Runner
from Modules.elmer import Elmer
from Modules.parametric_sweep import ParametricSweep

def main():

    ps = ParametricSweep(fun=parametricSweepFun)

    ps.getSweepDict(dict=testSweepDict)
    ps.getDicts(dicts=[initialDictConst, tranPropDict, elmerDict])
    ps.run()




def parametricSweepFun(name):
    oldpath = developedFlow(name)
    hartmann(oldpath, name)

def developedFlow(name):
    generalPath= os.getcwd()
    mc = Manipulations(base_path=basePathStep1)
    mc.create_name(name, 'solved', name_base=baseName1)  #return name
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName)
    runPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePathStep1, dist_path=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    initialClass = IntiailValue(pathCase=runPath)
    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    meshClass = Mesh(pathCase=runPath)


    sc.setControlDict(controlDict1)

    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiels(initialDictConst, initialDictCalculated)

    cpClass.setTurbModel2(turbType1)
    cpClass.setTransportProp(tranPropDict)


    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()

    rc = Runner(path_case=runPath)
    rc.setCoresOF(coreOF=coreOFstep1)
    rc.set_solver_name()
    rc.set_mode(mode=modeStep1)
    rc.set_pyFoam_settings(pyFoam=False)
    rc.setDecomposeParDict(nameVar=nameCoreOF)
    rc.runCase()

    os.chdir(generalPath)
    return os.path.abspath(runPath)


def hartmann(oldPath, name):
    generalPath = os.getcwd()
    mc = Manipulations(base_path=basePathStep2)  # initialize manipulation class
    mc.create_name(name, 'solved', name_base=baseName2)
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName, path_key='newPath')
    mc.create_path_dir(dirname=os.getcwd(), case_name=oldPath, path_key='oldPath')
    runPath = mc.get_path('newPath')
    oldPath = mc.get_path('oldPath')
    mc.duplicate_case(src_path=basePathStep2, dist_path=runPath, mode=modeManipul2)

    # initialization all required classes
    sc = SetSystem(pathCase=runPath)
    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    initialClass = IntiailValue(pathCase=runPath)
    meshClass = Mesh(pathCase=runPath)
    eClass = Elmer(pathCase=runPath, sifName='case.sif')
    rc = Runner(path_case=runPath)


    sc.setControlDict(controlDict2) # настраиваем controlDict
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
    rc.set_solver_name()  # set name of solver
    rc.set_mode(mode=mode2)  # set mode to run
    rc.set_pyFoam_settings(pyFoam=False)          # set to run pyFoam
    rc.setDecomposeParDict(nameVar=varcoreOF)       # write core to decomposeParDict

    # write settings for mapFields
    initialClass.settingsMapField(consistent=True, mapMethod='mapNearest', parallelSource=True,
                         parallelTarget=False, sourceTime=0.25)
    # create command mapFields
    initialClass.createMapFieldCommand()
    # run mapFields
    initialClass.mapFieldsRun(check=True)

    rc.decompose_OF(True)
    rc.decompose_Elmer(True)

    rc.runCase()   # run case
    os.chdir(generalPath)
    return os.path.abspath(runPath)


if __name__ == "__main__":
    main()