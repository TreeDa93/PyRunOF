import os, sys
modulesPath = '/home/ivan/mySolvers/RunnerForCases/'
sys.path.append(modulesPath)

from Modules.manipulations import Manipulations
from Modules.run import Runner
from Modules.meshes import Mesh
from Modules.set_system import SetSystem
from Modules.initial_value import InitialValue
from Modules.constant import SetConstantParam



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

    manipulationClass = Manipulations(base_path=basePath)

    #here just test functions###
    manipulationClass.create_path(basePath, path_key='SecondPath')
    manipulationClass.create_path(basePath, path_key='test')
    manipulationClass.get_path('basePath')
    manipulationClass.get_path('1223')  # it should be error for test
    manipulationClass.change_path('tesPathh', pat_key='test')
    manipulationClass.change_path('tesPathh', pat_key='123235')  # it should be error for test
    manipulationClass.create_name('test', name_base=basePath, name_key='testName')
    ###
    manipulationClass.create_name('solved', name_base=basePath)
    newName = manipulationClass.get_name('newName')
    manipulationClass.create_path_dir(dirname=os.getcwd(), case_name=newName)
    newPath = manipulationClass.get_path('newPath')
    manipulationClass.duplicate_case(base_path=basePath, new_path=newPath, mode='rewrite')



    systemClass = SetSystem(pathCase=newPath)
    systemClass.setControlDict(controlDict)
    systemClass.setfvSolution(controlDict) #test method
    systemClass.setfvSchemes(controlDict) #test method
    systemClass.setAnyFiles(controlDict) #test method


    meshClass = Mesh(pathCase=newPath)
    meshClass.setBlockMesh(meshList)
    meshClass.runBlockMesh()


    initValueClass = InitialValue(pathCase=newPath)
    newDict= initValueClass.calcInitVal(A, B, Uin, nu)
    initValueClass.setVarAllFiles(constDictVar, newDict)
###tests
    #initValueClass.setVarAllFiles()  # test
    #initValueClass.setVar(constDictVar, newDict)
    #initValueClass.setVar(constDictVar, newDict, nameFiels=['U', 'k'], path_case=newPath)
 ######

    constantClass = SetConstantParam(pathCase=newPath)
    constantClass.set_transportProp(tranPropDict)
    constantClass.setTurbModel(typeTurbModel='kEpsilon')


    runClass = Runner()
    runClass.setCores()
    runClass.setPathCase(newPath)
    runClass.set_solver_name()
    runClass.set_mode(mode='common')
    runClass.set_pyFoam_settings(pyFoam=False)
    runClass.runCase()


