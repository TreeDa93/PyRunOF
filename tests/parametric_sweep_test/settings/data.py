
import os 

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

coreOF = 4
solverName ='pimpleFoam'
mode = 'parallel'

dir_path = os.getcwd()
src_case = 'base_case'

data = {
        'nu_var': nu,
        'rho_var': rho,
        'startTime_var' : startTime,
        'endTime_var' : stopTime,
        "Uin_var": Uin,
        'L_var' : L,
        'A_var' : A,
        'B_var' : B,
        'hx_var' : hx,
        'hy_var' : hy,
        'hz_var' : hz,
        }

ps_params = {'Uin_var': [3, 2, 5, 1],
            'nu_var': [1e-07, 2e-07, 5e-07, 8e-07],
            'rho_var': [6450, 6410, 6100, 6500]}