import pyRunOF
import os.path
from settings.data import *


def main():
    ps = pyRunOF.ParametricSweep(fun=run)
    mp = settings_fun()
    ps.collect_information(mp)

    ps.run(mp.get_path('parameters_path'), ps_params, fun=run, type_set='special series')
    #delete_fun()

def run(ps):
    mp = pyRunOF.Manipulations(dir_path=dir_path)
    mp.collect_information(ps)
    ps.get_cur_name()
    mp.create_name(ps.get_cur_name(type_name='index'), name_base=src_case, name_key=dst_name_key)
    mp.create_path_dir(dir_path_key='solution', name_key=dst_name_key,
                       path_key=dst_path_key)
    mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')

    data = mp.get_dict_from_json(ps.get_cur_json_path())
    #data['U_var'] = calculate_velocity(data['Re_var'], data['nu_var'], data['d_var'])

    mp.change_json_params(ps.get_cur_json_path(), data)




    ########### System folder #######################
    system = pyRunOF.System(case_path=mp.get_path(dst_path_key))
    system.set_control_dict(data, case_path=mp.get_path(dst_path_key))

    ########### Constant folder #####################
    constant = pyRunOF.Constant(case_path=mp.get_path(dst_path_key), lib_path=library_path['lib_path_var'])
    constant.set_transportProp(data)

    ########### Initial conditions #####################
    zero = InitialValue(case_path=mp.get_path(dst_path_key))

    data.update(zero.calcInitVal_cylindr(data['d_var'], data['U_var'], data['nu_var']))
    zero.set_var(data, file_names=zero.find_all_zero_files(),
                 case_path=mp.get_path(dst_path_key)
                 )

    ########### mesh settings #####################
    mesh = Mesh(case_path=mp.get_path(dst_path_key))
    mesh.set_decomposePar(data)

    mp.create_name(name_base='create_obstacle_mesh.py', only_base=True, name_key='salome_script')
    mp.create_path_dir(dir_path_key='settings', name_key='salome_script', path_key='salome_script_path')
    poly_mesh_path = mp.get_constant_path(str(mp.get_path(dst_path_key))) / 'polyMesh'
    mp.change_json_params(ps.get_cur_json_path(), {'constant_path': str(poly_mesh_path)}) # add path for mesh save

    mesh.run_salome_mesh(script_path=mp.get_path('salome_script_path'), parameter_path=ps.get_cur_json_path())

    mesh.decompose_run_OF()
    runner = Run(solver='icoFoam', path_case=mp.get_path(dst_path_key))
    runner.set_log_flag(log_flag=True)
    runner.set_mode(mode='parallel')
    runner.set_cores(coreOF=8)
    runner.run()

def singl_run():
    mp = settings_fun()

    mp.create_name('test', name_base=src_case, name_key=dst_name_key)
    mp.create_path_dir(dir_path_key='solution', name_key=dst_name_key,
                       path_key=dst_path_key)

    mp.duplicate_case(src_key=src_path_key, dist_key=dst_path_key, mode='rewrite')

    data = mp.get_dict_from_json(mp.get_path('parameters_path'))

    # here update velocity according Re number
    # data['U_var'] = calculate_velocity(data['Re_var'], data['nu_var'], data['d_var'])
    # mp.change_json_params(mp.get_path('mesh_parameters_path'), data)

    ########### System folder #######################
    system = System(case_path=mp.get_path(dst_path_key))
    system.set_control_dict(data) #, case_path=mp.get_path(dst_path_key))

    ########### Constant folder #####################
    constant = Constant(case_path=mp.get_path(dst_path_key), lib_path=library_path['lib_path_var'])
    constant.set_transportProp(data)
    """
    LES - Large eddy simulation
                kEpsilon
                realizablekE
                kOmega
                kOmegaSST
                laminar
                LESSmag
    """

    constant.turbulent_model(turbulent_type='kEpsilon')  # , case_path=mp.get_path(dst_path_key))

    ########### Initial conditions #####################
    zero = InitialValue(case_path=mp.get_path(dst_path_key))

    data.update(zero.calcInitVal_cylindr(data['d_var'], data['U_var'], data['nu_var']))

    zero.set_var(data, file_names=zero.find_all_zero_files())
                 #case_path=mp.get_path(dst_path_key),
                 #)

    ########### mesh settings #####################
    mesh = Mesh(case_path=mp.get_path(dst_path_key))
    mesh.set_decomposePar(data)

    mp.create_name(name_base='create_obstacle_mesh.py', only_base=True, name_key='salome_script')
    mp.create_path_dir(dir_path_key='settings', name_key='salome_script', path_key='salome_script_path')
    poly_mesh_path = mp.get_constant_path(str(mp.get_path(dst_path_key))) / 'polyMesh'

    data.update({'constant_path': str(poly_mesh_path)})

    mp.create_path_dir(dir_path_key='settings', case_name='parameters.json',
                       path_key='parameters_path_new')

    # collect general dict of parameters и записывает в путь по ключу parameters_path
    mp.create_json_params(data, save_path=mp.get_path('parameters_path_new'))

    mesh.run_salome_mesh(script_path=mp.get_path('salome_script_path'),
                         parameter_path=mp.get_path('parameters_path_new'))

    mesh.decompose_run_OF()
    runner = Run(solver='pisoFoam', path_case=mp.get_path(dst_path_key))
    runner.set_log_flag(log_flag=True)
    runner.set_mode(mode='parallel')
    runner.set_cores(coreOF=data['core_OF'])
    runner.run()


def settings_fun():
    mp = Manipulations(dir_path=dir_path)
    ## Set path for folder with settings and solution
    mp.create_path_dir(dir_path_key='dir', case_name='settings',
                       path_key='settings')
    mp.create_path_dir(dir_path_key='dir', case_name='solution',
                       path_key='solution')
    # set path of source case
    mp.create_name(name_base=src_case, name_key=src_name_key)
    mp.create_path_dir(dir_path_key='settings', name_key=src_name_key,
                       path_key=src_path_key)
    # path to json parameters
    mp.create_path_dir(dir_path_key='settings', case_name='parameters.json',
                       path_key='parameters_path')
    # path to json parameters of mesh
    mp.create_path_dir(dir_path_key='settings', case_name='mesh_parameters.json',
                       path_key='mesh_parameters_path')
    # имя скрипта для создания сетки
    mp.create_name(name_base='create_obstacle_mesh.py', only_base=True, name_key='salome_script')
    # путь к скрипту сетки
    mp.create_path_dir(dir_path_key='settings', name_key='salome_script', path_key='salome_script_path')
    # set path to general parameters
    mp.create_path_dir(dir_path_key='settings', case_name='parameters.json',
                       path_key='parameters_path')
    # set path to general parameters
    mp.create_path_dir(dir_path_key='settings', case_name='mesh_parameters.json',
                       path_key='mesh_parameters_path')
    # collect general dict of parameters и записывает в путь по ключу parameters_path
    mp.create_json_params(time_dict, parallel_dict, prop_dict, zero_dict, library_path,
                          mp.get_dict_from_json(mp.get_path('mesh_parameters_path')),
                          save_path=mp.get_path('parameters_path'))

    if not os.path.exists(mp.get_path('solution')):
        mp.create_folder(dir_key='dir', folder_name='solution')
        print('create sol folder!!!')

    return mp

def delete_fun():
    mp = settings_fun()
    delte_status_sol = True
    delete_json_files = True
    delte_status_sol2 = True
    if delte_status_sol is True:
        mp.delete_cases([mp.get_path('solution')])
    if delete_json_files is True:
        mp.delete_cases(words=['parameters_'], directory=mp.get_path('settings'))
    if delte_status_sol2 is True:
        mp.delete_cases(words=['parameters_'], directory=mp.get_path('solution'))
def calculate_velocity(Re, nu, d):
    return Re / d * nu




if __name__ == "__main__":
    #main()
    singl_run()
