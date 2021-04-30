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
from Modules.ParametricSweep import ParametricSweep

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

    mc = Manipulations(basePath=basePathStep1)
    mc.generatorNewName(name, initialDictConst['Uin_var'], baseNewName='step1')
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





if __name__ == "__main__":
    main()