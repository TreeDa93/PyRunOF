
base_case = 'PoiseuilleFlow'


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

Uin = 1 # inlet velocity
nu = 3.7e-07 # kinematic visocosity
rho = 6440 # mass density
startTime = 0 # start time at controlDict
stopTime = 0.25 #stop time at controlDict

data = {
        'L_var' : L,
        'A_var' : A,
        'B_var' : B,
        'hx_var' : hx,
        'hy_var' : hy,
        'hz_var' : hz,
        'Uin_var': Uin,
        'startTime_var' : startTime,
        'endTime_var' : stopTime,
        "nu_var": nu,
        'rho_var': rho
        }

turbulence_model = 'kOmegaSST'

# data_test = {}
# for key, val in globals().items():
#     if '_var' in key:
#         data_test.update({key: val})