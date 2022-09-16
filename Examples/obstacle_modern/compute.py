import sys
libpath = '/home/ivan/PyRunOF/'
sys.path.append(libpath)
from Modules.manipulations import Manipulations
from Modules.set_system import System
from Modules.constant import Constant
from Modules.initial_value import InitialValue
from Modules.run import Run
from Modules.meshes import Mesh
from Modules.parametric_sweep import ParametricSweep
from settings.data import *


def main():
     # run_salome()
     # ps = ParametricSweep(fun=solution)
     # ps.set_sweep_dict(sweep_dict=sweep_dict)
     # ps.set_find_dicts(find_dicts=[zero_dict])
     # ps.run(generator_names=True)
     solution('test')


def run_salome():
    mp = Manipulations(dir_path=dir_path)
    mp.create_path_dir(dir_path_key='dir', case_name='settings', path_key='settings')
    from Modules.auxiliary_functions import Executer
    command = 'salome -t create_obstacle_mesh.py'
    Executer.run_command(command, mp.get_path('settings'))

def solution(name):
    ##############General manipualations ###################
    mp = Manipulations(dir_path=dir_path)
    mp.create_path_dir(dir_path_key='dir', case_name='settings', path_key='settings')
    mp.create_path_dir(dir_path_key='dir', case_name='solution', path_key='solution')

    mp.create_name(name_base=src_case, name_key=src_name_key)
    mp.create_path_dir(dir_path_key='settings', name_key=src_name_key, path_key=src_path_key)

    mp.create_name(name, name_base=src_case, name_key=dst_name_key)
    mp.create_path_dir(dir_path_key='solution', name_key=dst_name_key, path_key=dst_path_key)

    mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')

    ########### System folder #######################
    system = System(case_path=mp.get_path(dst_path_key))
    system.set_control_dict(time_dict, case_path=mp.get_path(dst_path_key))

    ########### Constant folder #####################
    constant = Constant(case_path=mp.get_path(dst_path_key), lib_path=libpath)
    constant.set_transportProp(prop_dict)

    ########### Initial conditions #####################
    zero = InitialValue(case_path=mp.get_path(dst_path_key))

    zero.set_var(zero_dict, file_names=zero.find_all_zero_files(),
                 case_path=mp.get_path(dst_path_key)
                 )
    ########### mesh settings #####################
    mesh = Mesh(case_path=mp.get_path(dst_path_key))
    mesh.set_decomposePar(parallel_dict)

    mp.create_name(name_base='create_obstacle_mesh.py', only_base=True, name_key='salome_script')
    mp.create_path_dir(dir_path_key='settings', name_key='salome_script', path_key='salome_script_path')
    mp.create_path_dir(dir_path_key='settings', case_name='parameters.json', path_key='parameters_path')
    mesh.create_salome_mesh(script_path=mp.get_path('salome_script_path'),
                            parameter_path=mp.get_path('parameters_path'))
    #mesh.set_salome_script_path(mp.get_path(path_key='salome_script_path'))

    #mesh.decompose_run_OF()

    runner = Run(solver='icoFoam', path_case=mp.get_path(dst_path_key))
    runner.set_mode(mode='parallel')
    runner.set_cores(coreOF=8)
    #runner.run()



if __name__ == "__main__":
    main()
