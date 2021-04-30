
basePath = 'pitzDaily'
solverName = 'pimpleFoam'


##########
###Data###############
##############3


"""
Additional variables
"""
Uin = 1 # inlet velocity
nu = 3.7e-07 # kinematic visocosity

startTime = 0 # start time at controlDict
stopTime = 0.25 #stop time at controlDict

# additional variables to initizialize intial values
constDictVar = {"Uin_var": Uin
                }

# variables for transportProperties
tranPropDict = {"nu_var": nu}

#list with variables for controlDict
controlDict = {'startTime_var' : startTime,
                'endTime_var' : stopTime
                }

coreOF = 4
