import os
import sys # import library
libpath = '/home/ivan/PyRunOF/' #write name to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes
from Modules.manipulations import Manipulations
from Modules.elmer import Elmer


def main():
    mc = Manipulations(dir_path=os.getcwd())
    mc.create_name(name_base='hartmann', name_key='base', only_base=True)
    mc.create_path_dir(case_name=mc.get_name('base'), path_key='base')
    mc.create_name(name_base='hartmann_dublicate', name_key='dublicate', only_base=True)
    mc.create_path_dir(case_name=mc.get_name('dublicate'), path_key='dublicate')
    print(f'Проверка опции получения пути с ключем base', mc.paths['base'])
    print(f'Проверка опции получения пути с ключем dublicate', mc.paths['dublicate'])

    mc.duplicate_case(src_key='base', dist_key='dublicate', mode='copy')
    elmer = Elmer(key='ElmerTest', case_path=mc.paths['dublicate'],
                  sif_name='case.sif')
    elmer_dict = {'Bm_var': 10} # создаем словарь с переменной
    elmer.set_var(elmer_dict) # проверка работы функции установки переменой в сиф файле

    print(elmer.find_all_sif())
    pathes, names = mc.find_folders_by_word(word='hartmann_', dir_key='dir')
    print(pathes)
    print(names)
    mc.delete_cases(words=['old'], dir_key='dir')
    #mc.delete_case(full_path=mc.paths['dublicate'])

    #elmer.set_path(path_case='new_path', info_key='new_key') #  test fun to set path in elmer_info
    #print(elmer.get_path(info_key='new_key'))
    #elmer.set_new_parameter(parameter='test_new_param', parameter_name='test_value_new_param')
    #print(elmer.elmer_info)
    #print(elmer.get_any_parameter(parameter_name='test_value_new_param'))


if __name__ == "__main__":
    main()