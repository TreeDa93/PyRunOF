"""Mesh and geometry parameters"""
import os

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
initialDictConst = {"Uin_var": Uin
                }

# variables for transportProperties
tranPropDict = {"nu_var": nu,
                'rho_var': rho}

#list with variables for controlDict
controlDict = {'startTime_var' : startTime,
                'endTime_var' : stopTime
                }
"""     LES
        kEpsilon
        realizableKE
        kOmega
        kOmegaSST
"""

turbType = 'kOmegaSST'

basePathStep1 = os.path.abspath('step1')
basePathStep2 = os.path.abspath('step2')

coreOF = 4
solverName ='pimpleFoam'
mode = 'parallel'