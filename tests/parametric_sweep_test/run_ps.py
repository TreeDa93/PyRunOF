import pyRunOF
from settings.data import *
from time import sleep

TEST_MODE = True
GENERATE_JSON_PARAMS = True
DELETE_SOL_FOLDER = False
DELETE_CASES = False

def main():
    ps = pyRunOF.ParametricSweep()
    ps.run_new(ps_params, fun=run_case, update_vars=(data, ), type_set='special series')

def run_case(ps):

    mp = pyRunOF.Manipulations(dir_path=dir_path)
    mp.create_path_from_dir(dir_path_key='dir', folder_name='settings', path_key='settings')
    mp.create_path_from_dir(dir_path_key='settings', folder_name=src_case, path_key='src')
    mp.create_path_from_dir(dir_path_key='dir', folder_name='solution', path_key='solution')

    if DELETE_SOL_FOLDER is True:
        mp.delete_cases(full_pathes=[mp.get_path('solution')])

    if DELETE_CASES is True:
        mp.delete_cases(words=['base_case'], directory=mp.get_path('solution'))

    mp.get_path('solution').mkdir(exist_ok=True)
    
    mp.create_name(ps.get_cur_name(type_name='index'), name_base=src_case, name_key='dst')
    mp.create_path_from_dir(dir_path_key='solution', folder_name_key='dst', path_key='dst')

    mp.duplicate_case(src_key='src', dist_key='dst', mode='rewrite')
    
    system = pyRunOF.System(case_path=mp.get_path('dst'))
    system.set_controlDict(data)
    
    init_val = pyRunOF.InitialValue(case_path=mp.get_path('dst'))
    # calculate intial values
    data.update(init_val.calcInitVal(data['A_var'], data['B_var'], data['Uin_var'], data['nu_var']))
    init_val.set_var(data)
    
    constant = pyRunOF.Constant(case_path=mp.get_path('dst'))
    constant.set_transportProp(data) 
    #constant.turbulent_model(turbulent_type='laminar')   
    
    mesh = pyRunOF.Mesh(case_path=mp.get_path('dst'))
    mesh.set_blockMesh(data)

    runner = pyRunOF.Run(case_path=mp.get_path('dst'),
                        solver=solverName,
                        mode='parallel', 
                        OF_core=coreOF,
                        )
    
    if GENERATE_JSON_PARAMS is True:
        json_name = f'params_{ps.cur_i}'
        mp.create_path_from_dir(dir_path_key='solution', folder_name=json_name, path_key='params')
    
    mp.create_json_params(data, save_path=mp.get_path('params'))
    if TEST_MODE is not True:
        mesh.run_blockMesh()
        runner.run()

if __name__ == '__main__':
    main()