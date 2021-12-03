import sys # import library
libpath = '/home/ivan/mySolvers/RunnerForCases/' #write name to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes

from data import * # import variables from data

# add require modules from pyRunOF library
from Modules.manipulations import Manipulations
from Modules.meshes import Mesh
from Modules.set_system import System
from Modules.initial_value import IntiailValue
from Modules.constant import Constant
from Modules.run import Runner
from Modules.parametric_sweep import ParametricSweep

def main():

    ps = ParametricSweep(fun=step1)
    ps.setFun(step1)

    testSweepDict = {'Uin_var': [3, 2, 5, 1],
                     'nu_var': [1e-07, 2e-07, 5e-07, 8e-07],
                     'rho_var': [6450, 6410, 6100, 6500]}
    ps.getSweepDict(dict=testSweepDict)
    ps.getDicts(dicts=[initialDictConst, tranPropDict])
    ps.run()







def step1(name):

    mc = Manipulations(base_path=basePathStep1)
    mc.create_name(name, initialDictConst['Uin_var'], name_base='step1')
    newName = mc.get_name('newName')
    mc.create_path_dir(dirname=os.getcwd(), case_name=newName)
    runPath = mc.get_path('newPath')
    mc.duplicate_case(src_path=basePathStep1, dist_path=runPath, mode='rewrite')

    sc = System()
    sc.setControlDict(controlDict)

    initialClass = IntiailValue(pathCase=runPath)
    initialDictCalculated= initialClass.calcInitVal(A, B, Uin, nu)
    initialClass.setVarAllFiels(initialDictConst, initialDictCalculated)

    cpClass = Constant(case_path=runPath)
    cpClass.setTurbModel(turbType)
    cpClass.setTransportProp(tranPropDict)

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





if __name__ == "__main__":
    main()