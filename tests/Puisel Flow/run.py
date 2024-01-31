import pathlib as pl
import pyRunOF
from data import *


def main():
    mp = pyRunOF.Manipulations()
    mp.create_path_from_dir(dir_path=pl.Path.cwd(), folder_name=base_case, path_key='src')
    mp.create_name('solved', name_base=base_case, name_key='dst')
    mp.create_path_from_dir(dir_path=pl.Path.cwd(), folder_name_key='dst', path_key='src')
    
    mp.duplicate_case(src_key='src', dist_key='dst', mode='rewrite')


    system = pyRunOF.System(case_path=mp.get_path('dst'))
    system.set_controlDict(data)

    mesh = pyRunOF.Mesh(case_path=mp.get_path('dst'))
    mesh.set_blockMesh(data)

    init_val = pyRunOF.InitialValue(case_path=mp.get_path('dst'))
    data_aux = init_val.calcInitVal(A, B, Uin, nu)
    init_val.set_var(data, data_auxa)

    constant = pyRunOF.Constant(case_path=mp.get_path('dst'))
    constant.set_transportProp(data)
    constant.turbulent_model(turbulent_type='kEpsilon')

    mesh.run_blockMesh()
    
    runner = pyRunOF.Run(case_path=mp.get_path('dst'),
                         solver='pimpleFoam',
                         )
    runner.run()

if __name__ == "__main__":

    main()