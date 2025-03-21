import pyRunOF
import os.path
from settings.data import *


def main():
    
    # Initialize a class to process case. Here we declare path of working folder
    mp = pyRunOF.ModelConfigurator(dir_path=dir_path)

    ## Set path for folder with settings and solution
    mp.create_path_from_dir(dir_path_key='dir', folder_name='settings',
                        path_key='settings')
    mp.create_path_from_dir(dir_path_key='dir', folder_name='solution',
                        path_key='solution')

    # set path of source case
    mp.create_name(name_base=src_case, name_key=src_name_key)
    mp.create_path_from_dir(dir_path_key='settings', name_key=src_name_key,
                        path_key=src_path_key)
    # set path of dst case
    mp.create_name('test', name_base=src_case, name_key=dst_name_key)
    mp.create_path_from_dir(dir_path_key='solution', name_key=dst_name_key,
                        path_key=dst_path_key)
        
    # path to json parameters
    mp.create_path_from_dir(dir_path_key='settings', folder_name='parameters.json',
                        path_key='parameters_path')
    # path to json parameters of mesh
    mp.create_path_from_dir(dir_path_key='settings', folder_name='mesh_parameters.json',
                        path_key='mesh_parameters_path')
    
    # имя скрипта для создания сетки
    mp.create_name(name_base='create_obstacle_mesh.py', only_base=True, name_key='salome_script')
    # путь к скрипту сетки
    mp.create_path_from_dir(dir_path_key='settings', name_key='salome_script', path_key='salome_script_path')

    poly_mesh_path = mp.get_constant_path(str(mp.get_path(dst_path_key))) / 'polyMesh'

    # collect general dict of parameters и записывает в путь по ключу parameters_path
    mp.create_json_params(time_dict, parallel_dict, prop_dict, zero_dict, library_path,
                            mp.get_dict_from_json(mp.get_path('mesh_parameters_path')),
                            save_path=mp.get_path('parameters_path'))
    
    data = mp.get_dict_from_json(mp.get_path('parameters_path'))

    data.update({'constant_path': str(poly_mesh_path)})
    # collect general dict of parameters и записывает в путь по ключу parameters_path
    mp.create_json_params(data, save_path=mp.get_path('parameters_path'))

    # if the solution folder does not exist we create it by below written code
    if not os.path.exists(mp.get_path('solution')):
        mp.create_folder(dir_key='dir', folder_name='solution')

    mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')

    ########### case settings #####################
    system = pyRunOF.System(case_path=mp.get_path(dst_path_key))
    system.set_controlDict(data)
    constant = pyRunOF.Constant(case_path=mp.get_path(dst_path_key), lib_path=library_path['lib_path_var'])
    constant.set_transportProp(data)
    zero = pyRunOF.InitialValues(case_path=mp.get_path(dst_path_key))
    zero.set_var(data,)
    ########### mesh settings #####################
    mesh = pyRunOF.Mesh(case_path=mp.get_path(dst_path_key))
    mesh.set_decomposePar(data)
    mesh.run_salome_mesh(script_path=mp.get_path('salome_script_path'),
                        parameter_path=mp.get_path('parameters_path'))
    mesh.run_decompose(what='OF')
    ########### run settings #####################
    runner = pyRunOF.Run(solver='icoFoam', case_path=mp.get_path(dst_path_key))
    runner.set_log_flag(log_flag=True)
    runner.set_mode(mode='parallel')
    runner.set_cores(coreOF=data['core_OF'])
    runner.run()

if __name__ == "__main__":
    main()