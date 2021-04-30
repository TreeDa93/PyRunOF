import os, sys
modulesPath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(modulesPath)

from Modules.Manipulations import Manipulations
from Modules.RunApplication import Runner
from Modules.Meshes import Mesh
from Modules.setSystem import SetSystem
from Modules.InitialValue import IntiailValue
from Modules.setConstant import SetConstantParam



#basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/pimpleFoam/cavity/cavity'
#basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/pimpleFoam/RAS/pitzDaily'
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

    manipulationClass = Manipulations(basePath=basePath)

    #here just test functions###
    manipulationClass.createYourPath(basePath, keyPath='SecondPath')
    manipulationClass.createYourPath(basePath, keyPath='test')
    manipulationClass.getPath('basePath')
    manipulationClass.getPath('1223') # it should be error for test
    manipulationClass.changePath('tesPathh', keyPath='test')
    manipulationClass.changePath('tesPathh', keyPath='123235') # it should be error for test
    manipulationClass.generatorNewName('test', baseNewName=basePath, keyName='testName')
    ###
    manipulationClass.generatorNewName('solved', baseNewName=basePath)
    newName = manipulationClass.getName('newName')
    manipulationClass.createNewPath(dirmame=os.getcwd(), newCaseName=newName)
    newPath = manipulationClass.getPath('newPath')
    manipulationClass.dublicateCase(basePath=basePath, newPath=newPath, mode='rewrite')



    systemClass = SetSystem(pathCase=newPath)
    systemClass.setControlDict(controlDict)
    systemClass.setfvSolution(controlDict) #test method
    systemClass.setfvSchemes(controlDict) #test method
    systemClass.setAnyFiles(controlDict) #test method


    meshClass = Mesh(pathCase=newPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()


    initValueClass = IntiailValue(pathCase=newPath)
    newDict= initValueClass.calcInitVal(A, B, Uin, nu)
    initValueClass.setVarAllFiels(constDictVar, newDict)
###tests
    #initValueClass.setVarAllFiels()  # test
    #initValueClass.setVar(constDictVar, newDict)
    #initValueClass.setVar(constDictVar, newDict, nameFiels=['U', 'k'], pathCase=newPath)
 ######

    constantClass = SetConstantParam(pathCase=newPath)
    constantClass.setTransportProp(tranPropDict)
    constantClass.setTurbModel(typeTurbModel='kEpsilon')


    runClass = Runner()
    runClass.setCores()
    runClass.setPathCase(newPath)
    runClass.setNameSolver(solverName='pimpleFoam')
    runClass.setModeRunner(mode='common')
    runClass.setPyFoamSettings(pyFoam=False)
    runClass.runCase()


