import os

library_path = {'lib_path_var': '/home/ivan/PyRunOF/'}

###############
###Parameters###
################
###### directories#####
#dir_path = os.path.join(os.getcwd(), 'Examples', 'obstacle_turb_models_pisoFoam_in_progress')
dir_path = os.getcwd()
src_case = 'obstacle_base_turb'
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
             'endTime_var': 150,
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

"""
    "d_var": 0.01, - диаметр припятсвия
   "betta_var": 0.25, - отношение диаметра препятсвия к высотек канала d/h от 0.1 до 0.4
   "nC_var": 360, # количество точек по окружности препятсвияnumSegmentsCircle [120, 180, 260, 300, 360]
   "Ha_var": 2160, 
   "circle_layer_var": 0.01,
   "nWall_layer_var": 20, - количество элементов в шерклифовском слое [7, 10, 15, 16, 20]
   "nCircle_layer_var": 96, - количество элементов в слое возле препятсвия [32, 56, 72, 80]
   "k_wall_var": 1.03,
   "max_size_elem_var": 3e-4, 
   "min_size_elem_var": 1e-8,
   "k_global_var": 0.1,
   "quad_elem_var": true

"""

ps_params = {'nC_var': [120, 120, 120, 360, 360, 360],
             'max_size_elem_var': [1e-3,1e-3, 1e-3, 5e-4, 5e-4, 5e-4],
             'nWall_layer_var': [7, 7, 7, 20, 20, 20],
             'nCircle_layer_var': [32, 32, 32, 80, 80, 80],
             'deltaT_var': [0.05, 0.01, 0.005, 0.05, 0.01, 0.005]}

# ps_params = {'nC_var': [360], 'max_size_elem_var': [5e-4,],
#              'nWall_layer_var': [20], 'nCircle_layer_var': [80]}

#ps_params = {'Re_var': [10, 100, 300, 500, 1e4]}

# ps_params = {'nC_var': [120, 180, 260, 300, 360], 'max_size_elem_var': [1e-3, 9e-4, 6e-4, 3e-4, 3e-4],
#              'nWall_layer_var': [7, 10, 15, 16, 20], 'nCircle_layer_var': [32, 56, 72, 80, 96]}
