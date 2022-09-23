import sys
import os
libpath = '/home/ivan/PyRunOF/'
sys.path.append(libpath)
from Modules.manipulations import Manipulations
dir_path = os.getcwd()

def main():
    mp = Manipulations(dir_path=dir_path)
    mp.create_path_dir(case_name='parameters.json', path_key='parameters_path')
    mp.create_path_dir(case_name=f'parameters_test.json', path_key='parameters_path_new')

    mp.create_json_params(parameter_dict={}, save_path=mp.get_path('parameters_path'))
    mp.create_json_params({'var1': 2, 'var2': 3}, save_path=mp.get_path('parameters_path_new'))



if __name__ == "__main__":
    main()