import pyRunOF
import pathlib as pl
from pyRunOF.additional_fun.auxiliary_functions import run_command

TEST_MODE = True
EXAMPLE_ROOT = pl.Path(__file__).resolve().parent

def main():
    delete_status = 'no'

    mp = pyRunOF.ModelConfigurator(dir_path=EXAMPLE_ROOT)
    mp.create_path_from_dir(dir_path_key='dir', folder_name='planarCouette',
                       path_key='base_case')
    mp.create_path_from_dir(dir_path_key='dir', folder_name='planarCouette_solved',
                       path_key='sol_case')
    print(mp.get_path('sol_case'))

    if delete_status == 'ok':
        mp.delete_cases(words=['_solved'],
                        directory=mp.get_path('dir'))

    mp.duplicate_case(src_key='base_case', dist_key='sol_case')
    if TEST_MODE is False:
        run_command('./Allclean',mp.get_path('sol_case'))
        run_command('./Allrun',mp.get_path('sol_case'))



if __name__ == "__main__":
    print(EXAMPLE_ROOT)
    main()