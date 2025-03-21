
import pyRunOF as pRF
import os
import pathlib as pl

TEST_PATH = pl.Path().cwd() / 'tests / model_config_test'

def init_ModelConfigurator():
    mc = pRF.ModelConfigurator(dir_path=TEST_PATH, info_key='main')


def test_info_dict():
    mc = pRF.ModelConfigurator(dir_path=TEST_PATH, info_key='main')
    print('________ \n \n TEST: info dict  \n')
    print(mc.info)
    print('________ \n \n TEST: find_folders_by_word \n ')


def test_delete():
    mc = pRF.ModelConfigurator(dir_path=TEST_PATH, info_key='main')
    mc.create_name(name_base='source', 
                   only_base=True, name_key='src')
    mc.create_name(name_base='distination', 
                   only_base=True, name_key='dst')
    mc.create_path_from_dir(dir_path_key='dir', 
                            folder_name_key='src', 
                            path_key='src')
    mc.create_path_from_dir(dir_path_key='dir', 
                            folder_name_key='dst', 
                            path_key='dst')

    mc.create_folder_by_path(path_key='src')
    mc.create_folder_by_path(path_key='dst')
# # test find_folders_by_word
# print(mc.find_folders_by_word('www', directory=os.getcwd()))

# print('________ \n \n TEST: acces to info dict  \n')
# print(mc.info['main']['paths'])


# print('________ \n \n TEST: get_path  \n')
# print(mc.get_path('dir'))


# print('________ \n \n TEST: create_path  \n')
# mc.create_path(mc.get_path('cwd') / 'src', path_key='src')
# print(mc.get_path('src'))
# mc.create_folder_by_path(path_key='src')

# mc.create_path(mc.get_path('cwd') / 'dst', path_key='dst')
# print(mc.get_path('dst'))


# print('________ \n \n TEST: duplicate_case  \n')
# mc.duplicate_case(src_key='src', dist_key='dst', mode='copy')



# mc.delete_cases(mc.get_path('src'))
# mc.delete_cases(mc.get_path('dst'))

# mc.find_folders_by_word('sol', directory='resss')
# mc.create_name('test_folder', name_key='dir')
# mc.create_path('test', path=mc.get_path('dir'))

# test.create_path_from_dir()

# test.duplicate_case()


if __name__ == "__main__":
    init_ModelConfigurator()
    test_info_dict()