import os
from Modules.Manipulations import Manipulations
from Modules.RunApplication import Runner
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import IntiailValue
from Modules.setConstant import SetConstantParam

testPath = os.path.abspath('newTest')
basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/pimpleFoam/cavity/cavity'
basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/pimpleFoam/RAS/pitzDaily'
basePath = 'step2'
#pimpleFoam/RAS/pitzDaily/

##########
###Data###############
##############3
"""Mesh and geometry parameters"""
L = 0.1 # length of the duct
A = 0.01 # hiegh of the duct
B = 0.02 # width of the dcut
hx  = 40 # the number of cells along x
hy = 30 # the number of cells along y
hz  = 30 # the number of cells along z
# lsit with varibles for blockMeshDict
meshList = {'L_var' : L,
                    'A_var' : A,
                    'B_var' : B,
                    'hx_var' : hx,
                    'hy_var' : hy,
                    'hz_var' : hz,
                    }
"""
Additional variables
"""
Uin = 1 # inlet velocity
nu = 3.7e-07 # kinematic visocosity
rho = 6440 # mass density
startTime = 0 # start time at controlDict
stopTime = 0.25 #stop time at controlDict

# additional variables to initizialize intial values
constDictVar = {"Uin_var": Uin
                }

# variables for transportProperties
tranPropDict = {"nu_var": nu,
                'rho_var': rho}

#list with variables for controlDict
controlDict = {'startTime_var' : startTime,
                'endTime_var' : stopTime
                }
"""LES
        kEpsilon
        realizableKE
        kOmega
        kOmegaSST
"""

turbType = 'kOmegaSST'

if __name__ == "__main__":

    manipulationClass = Manipulations()
    manipulationClass.generatorNewNameFolder('solved', baseNewCase=basePath)
    manipulationClass.createNewPath(dirmame=os.getcwd(), newCaseName=manipulationClass.newNameCase)
    manipulationClass.dublicateCase(baseCasePath=basePath, newPath=manipulationClass.newPath, mode='rewrite')


"""
    systemClass = SetSystem(manipulationClass.newPath)
    systemClass.setControlDict(controlDict)

    meshClass = Mesh(pathNewCase=manipulationClass.newPath)
    meshClass.setBlockMesh(meshList)
    meshClass.createOFMesh(manipulationClass.newPath)

    initValueClass = IntiailValue(pathNewCase=manipulationClass.newPath)
    newDict= initValueClass.calcInitVal(A, B, Uin, nu)
    initValueClass.setVariablesValue(constDictVar, newDict)

    constantClass = SetConstantParam(pathNewCase=manipulationClass.newPath)
    constantClass.setTransportProp(tranPropDict)
    constantClass.setTurbModel(typeTurbModel='kEpsilon')

    runClass = Runner()
    runClass.setCores()
    runClass.setNewPathCase(manipulationClass.newPath)
    runClass.setNameSolver(solverName='pimpleFoam')
    runClass.setModeRunner(mode='common')
    runClass.setPyFoamSettings(pyFoam=False)
    runClass.runCase()
"""

