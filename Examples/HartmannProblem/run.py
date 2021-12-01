import sys # import library
libpath = '/home/ivan/mySolvers/pyFoamRun/' #write name to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes
/home/ivan/mySolvers/pyFoamRun/step1_solved
from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.manipulations import Manipulations
from Modules.meshes import Mesh
from Modules.set_system import SetSystem
from Modules.initial_value import InitialValue
from Modules.constant import SetConstantParam
from Modules.run import Run

def main():




    #step2(step1())
    oldpath = 'step1_solved'
    step2(oldpath)






def step1():
    generalPath= os.getcwd()
    mc = Manipulations(base_path=basePathStep1)
    mc.create_name(prefixName, name_base=baseName1)  #return name
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName)
    runPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePathStep1, dist_path=runPath, mode='rewrite')

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = InitialValue(pathCase=runPath)
    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiles(initialDictConst, initialDictCalculated)

    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    cpClass.setTurbModel2(turbType1)
    cpClass.set_transportProp(tranPropDict)

    meshClass = Mesh(case_path=runPath)
    meshClass.set_blockMesh(meshList)
    meshClass.run_blockMesh()

    rc = Runner(path_case=runPath)
    rc.setCoresOF(coreOF=coreOFstep1)
    rc.set_solver_name()
    rc.set_mode(mode=modeStep1)
    rc.set_pyFoam_settings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar=nameCoreOF)
    rc.runCase()

    os.chdir(generalPath)
    return os.path.abspath(runPath)



def step2(oldPath):
    generalPath = os.getcwd()
    mc = Manipulations(base_path=basePathStep2)
    mc.create_name(prefixName2, name_base=baseName2)
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName, path_key='newPath')
    mc.create_path_dir(dirname=os.getcwd(), case_name=oldPath, path_key='oldPath')
    runPath = mc.get_path('newPath')
    oldPath = mc.get_path('oldPath')
    mc.duplicate_case(src_path=basePathStep2, dist_path=runPath, mode=modeManipul2)

    sc = SetSystem(pathCase=runPath)
    sc.setControlDict(controlDict)

    initialClass = InitialValue(pathCase=runPath)
    initialClass.setMappSettings(sourcePath=oldPath, distPath=runPath, source='0.25', dist='0')
    initialClass.copyBC(nameBCsource='outlet', nameBCdist='inlet',
                                mapTimeStep=stopTime)
    initialClass.reconstruct(oldPath)
    initialClass.setMappValues()

    cpClass = SetConstantParam(pathCase=runPath, pathLib=libpath)
    cpClass.setTurbModel2(turbType1)
    cpClass.set_transportProp(tranPropDict)


    meshClass = Mesh(case_path=runPath)
    meshClass.set_blockMesh(meshList)
    meshClass.run_blockMesh()

    rc = Runner(path_case=runPath)
    rc.setCoresOF(coreOF=coreOF)
    rc.set_solver_name()
    rc.set_mode(mode=mode)
    rc.set_pyFoam_settings(pyFoam=False)
    rc.setDecomposeParDict(coreOF, nameVar='core_OF')
    rc.runCase()
    os.chdir(generalPath)
    return os.path.abspath(runPath)



def developedFlow():
    step3(step2(step1()))

if __name__ == "__main__":
    main()