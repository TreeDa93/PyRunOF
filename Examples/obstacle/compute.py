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

    ps = ParametricSweep(fun=solution)
    ps.set_sweep_dict(sweep_dict=sweep_dict)
    ps.set_find_dicts(find_dicts=[zero_dict])
    ps.run(generator_names=True)


def run_salome():
    mp = Manipulations(dir_path=dir_path)
def solution(name):
    ##############General manipualations ###################
    mp = Manipulations(dir_path=dir_path)
    mp.create_name(name_base=src_case, name_key=src_name_key)
    mp.create_path_dir(dir_path_key='dir', name_key=src_name_key, path_key=src_path_key)
    mp.create_name(name, name_base=src_case, name_key=dst_name_key)
    mp.create_path_dir(dir_path_key='dir', name_key=dst_name_key, path_key=dst_path_key)
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

    mesh = Mesh(case_path=mp.get_path(dst_path_key))
    mesh.set_decomposePar(parallel_dict)
    mesh.decompose_run_OF()

    runner = Run(solver='icoFoam', path_case=mp.get_path(dst_path_key))
    runner.set_mode(mode='parallel')
    runner.set_cores(coreOF=8)
    runner.run()



if __name__ == "__main__":
    main()
