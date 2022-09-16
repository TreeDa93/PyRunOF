import os

###############
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
                     the time steps to coincide with the writeInterval if necessary - used 
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
             'endTime_var': 2,
             'deltaT_var': 1e-1,
             'writeControl_var': 'adjustableRunTime',
             'writeInterval_var': 1,
             'runTimeModifiable_var': 'false',
             'adjustTimeStep_var': 'yes',
             'maxCo_var': 1,
             'maxDeltaT_var': 1
             }
###########Parallel############3

parallel_dict = {'core_OF': 8,
                'method_var': 'scotch'
                 }
############Properties #############
prop_dict = {'nu_var': 3.4e-7}
###########Initial values ##########
zero_dict = {'U_var': 34e-4}
############Parametric sweep #######
sweep_dict = dict(U_var=[1e-3, 1e-2])