import sys
import os
from Modules.manipulations import Manipulations
from Modules.set_system import System
from Modules.constant import Constant

libpath = '/home/ivan/PyRunOF/'
sys.path.append(libpath)
################
###Parameters###
################
###### directories#####
#dir_path = os.path.join(os.getcwd(), 'Examples', 'obstacle')
dir_path = os.getcwd()
src_case = 'obstacle_base'
src_name_key = 'src_name'
src_path_key = 'src_path'
dst_name_key = 'dst_name'
dst_path_key = 'dst_path'
#############################
###########Time##############
"""
startFrom_var : startTime, 'firstTime', latestTime
stopAt_var : endTime, writeNowm noWriteNow, writeControl
endTime_var : 360  s
deltaT_var : 1e-4 s
writeControl_var : timeStep - Writes data every writeInterval time steps
                    runTime: Writes data every writeInterval seconds of simulated time. 
                     adjustableRunTime: Writes data every writeInterval seconds of simulated time, adjusting 
                     the time steps to coincide with the writeInterval if necessary — used 
                     in cases with automatic time step adjustment
 writeInterval_var : 20 - Scalar used in conjunction with writeControl described above          
adjustTimeStep : yes or not - control by maxCo or other parameters
runTimeModifiable_var : yes or no runTimeModifiable_var : true or false 
                        - switch for whether dictionaries, e.g.controlDict, are re-read 
                        by OpenFOAM at the beginning of each time step. 
"""

time_dict = {'startFrom_var': 'startTime',
             'startTime_var': 0,
             'stopAt_var': 'endTime',
             'endTime_var': 360,
             'deltaT_var': 1e-4,
             'writeControl_var': 'adjustableRunTime',
             'writeInterval_var': 1,
             'runTimeModifiable_var': 'false',
             'adjustTimeStep_var': 'yes',
             'maxCo_var': 1,
             'maxDeltaT_var': 1
             }

###########Parallel############3

prallel_dict = {'core_OF': 8,
                'method_var': 'scotch'
                }
############Properties #############
prop_dict = {'nu_var': 3.4e-7}

mp = Manipulations(dir_path=dir_path)
mp.create_name(name_base=src_case, name_key=src_name_key)
mp.create_path_dir(dir_path_key='dir', name_key=src_name_key, path_key=src_path_key)
mp.create_name('test', name_base=src_case, name_key=dst_name_key)
mp.create_path_dir(dir_path_key='dir', name_key=dst_name_key, path_key=dst_path_key)
mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')
system = System(case_path=mp.get_path(dst_path_key))
system = System()
system.set_control_dict(time_dict, case_path=mp.get_path(dst_path_key))
system.set_any_files(prallel_dict, files=['decomposeParDict'])
constant = Constant(case_path=mp.get_path(dst_path_key), lib_path=libpath)
#constant.set_transportProp(prop_dict)

# def main():
#     mp = Manipulations(dir_path=dir_path)
#     mp.create_name(name_base=src_case, name_key=src_name_key)
#     mp.create_path_dir(dir_path_key='dir', name_key=src_name_key, path_key=src_path_key)
#     mp.create_name('test', name_base=src_case, name_key=dst_name_key)
#     mp.create_path_dir(dir_path_key='dir', name_key=dst_name_key, path_key=dst_path_key)
#     mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')
#     system = System(case_path=mp.get_path(dst_path_key))
#
#     system.set_control_dict(time_dict)
#     system.set_any_files(prallel_dict, files=['decomposeParDict'])
#     constant = Constant(case_path=mp.get_path(dst_path_key), lib_path=libpath)
#     constant.set_transportProp(prop_dict)



# if __name__ is '__main__':
#     main()
