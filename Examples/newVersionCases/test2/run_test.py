import sys  # import library
import os
# libpath = 'C:\\Users\\Ivan\\science\\works\\PyFoam\\PyRunOF' #write name to pyRunOF library
libpath = '/home/ivan/PyRunOF'
sys.path.append(libpath)  # add the library into system pathes
from Modules.manipulations import Manipulations
from Modules.set_system import SetSystem
from Modules.run import Run


def main():
    mc = Manipulations(dir_path=os.getcwd())
    mc.create_name('run', name_base='run_case', name_key='run', only_base=True)
    mc.create_name('base', name_base='pitzDaily', name_key='base', only_base=True)
    mc.create_path_dir(dir_path=os.getcwd(), case_name=mc.get_name('run'), path_key='run')
    mc.create_path_dir(dir_path=os.getcwd(), case_name=mc.get_name('base'), path_key='base')
    print(mc.paths['run'])
    print(mc.paths['base'])
    mc.duplicate_case(src_key='base', dist_key='run', mode='rewrite')

    #sc = SetSystem(case_path=mc.get_path('run'))
    #sc.set_control_dict({'end_time_var': 5})
    sc2 = SetSystem()
    sc2.set_control_dict_test({'endTime': 25}, case_path=mc.get_path('run'))

    run = Run(name='my_test', path_case=mc.get_path('run'),
              solver_name='pimpleFoam', mode='parallel'
              )
    run.set_decomposeParDict()
    #run.run()
    # mc.duplicate_case(src_path=mc.get_path('base'), dist_path=mc.get_path('run'))


if __name__ == "__main__":
    main()
