import os
import pyRunOF

# Input data
data = {'Uin_var': 1,
        'nu_var': 3.7e-07,
        'startTime_var': 0,
        'endTime_var': 0.25,
        'core_OF': 4
        }

if __name__ == "__main__":

    mp = pyRunOF.Manipulations(dir_path=os.getcwd())

    mp.create_path_dir(dir_path_key='dir', case_name='pitzDaily',
                       path_key='base_case')
    mp.create_path_dir(dir_path_key='dir', case_name='pitzDaily_solved',
                       path_key='solved_case')

    mp.duplicate_case(src_key='base_case', dist_key='solved_case', mode='rewrite')

    system = pyRunOF.System(case_path=mp.get_path('solved_case'))
    system.set_controlDict(data)
    init_val = pyRunOF.InitialValue(case_path=mp.get_path('solved_case'))
    init_val.set_var(data)
    constant = pyRunOF.Constant(case_path=mp.get_path('solved_case'))
    constant.set_transportProp(data)

    mesh = pyRunOF.Mesh(case_path=mp.get_path('solved_case'))
    mesh.set_decomposePar(data)
    mesh.run_blockMesh()
    mesh.run_decompose(what='OF')

    runner = pyRunOF.Run(solver='pimpleFoam', case_path=mp.get_path('solved_case'))
    runner.set_cores(coreOF=4)
    runner.set_mode(mode='parallel')
    runner.run()



