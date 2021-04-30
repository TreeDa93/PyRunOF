"""Mesh and geometry parameters"""
import os


"""

            
        *
z0,y2  /---z1, y2-----/z2, y2              
      /      y1      /
     /              / 
 z0 /--- z1, y0---- /z2

"""


scale = 1

L = 10 # length of the duct
A = 1 # hiegh of the duct
B = 2 # width of the dcut

z1 = 0
z0 = z1 - B/2
z2 = z1 + B/2
y1 = 0
y0 = y1 - A/2
y2 = y1 + A/2
x0 = 0
x1 = L

hx  = 50 # the number of cells along x
hy = 40 # the number of cells along y
hz  = 80 # the number of cells along z

kx = 1
ky = 4
kz = 4
kyback = 1/ky
kzback = 1/kz

# lsit with varibles for blockMeshDict
meshList = {'scale_var': scale,
            'z1_var':z1,'z0_var':z0,'z2_var':z2,
            'y1_var':y1,'y0_var':y0,'y2_var':y2,
            'x0_var':x0,'x1_var':x1,
            'hx_var' : hx,'hy_var' : hy, 'hz_var' : hz,
            'kx_var':kx,'ky_var':ky,'kz_var':kz, 'kyback_var': kyback,'kzback_var': kzback
                    }

elmerMeshDict= {'w_var': B,
                'h_var': A,
                'L_var': L,
               'hx_var': hx, 'hy_var': hy, 'hz_var': hz,
                'k_var': kx
                }



"""
Additional variables
"""
Uin = 1 # inlet velocity
nu = 1e-4 # kinematic visocosity
rho = 1 # mass density
Bm = 2

elmerDict = {'Bm_var': Bm}
# additional variables to initizialize intial values
initialDictConst = {"Uin_var": Uin}

# variables for transportProperties
tranPropDict = {"nu_var": nu,
                'rho_var': rho}

startTime1 = 0 # start time at controlDict
stopTime1 = 0.25 #stop time at controlDict
startTime2 = 0 # start time at controlDict
stopTime2 = 0.25 #stop time at controlDict
writeInterval = 0.05
#list with variables for controlDict
controlDict1 = {'startTime_var': startTime1,
                'endTime_var': stopTime1
                }
controlDict2 = {'startTime_var': startTime2,
                'endTime_var': stopTime2,
                'writeInterval_var': writeInterval}

#step 1###
basePathStep1 = os.path.abspath('LESbase')
prefixName = 'realizableKE'
baseName1 = 'developed'
modeStep1 = 'parallel'
solverName1 = 'pimpleFoam'
coreOFstep1 = 4
nameCoreOF = 'core_OF'
turbType1 = 'realizableKE'#'LESSmag'

#step 2###

basePathStep2 = os.path.abspath('hartmann')
prefixName2 = 'LES'
baseName2 = 'hartmann'
modeManipul2 = 'rewrite'

coreOF2 = 4
varcoreOF = 'core_OF'
coreElmer2 = 4
solverName ='mhdPimpleFoam'
mode2 = 'EOF'  #parallel ,common , EOF

