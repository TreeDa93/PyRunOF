import sys # import library
import os
#libpath = 'C:\\Users\\Ivan\\science\\works\\PyFoam\\PyRunOF' #write name to pyRunOF library
libpath = '/home/ivan/PyRunOF'
sys.path.append(libpath)  # add the library into system pathes
from Modules.manipulations import Manipulations


def main():
    pass

mc = Manipulations(dir_path=os.getcwd())
#mc = Manipulations()
#test names
mc.create_name('new', name_base='base_name')
mc.create_name('base', name_base='base_name', name_key='base')
mc.create_name('run', name_base='base_name', name_key='run')
mc.get_name('new')
mc.get_name('base')
mc.get_name('run')
#mc.get_name('false')

mc.create_name('test2', '1', '3', name_base='base1', name_key='test2')
mc.get_name('test2')

# test paths
mc.create_path_dir(dir_path=os.getcwd(), case_name='test', path_key='dir_path_test')
mc.create_path_dir(dir_path=os.getcwd(), name_key='new', case_name=None, path_key='dir_path_test2')
#mc.create_path_dir(dir_path=None, case_name='test', key='dir_path_test')
print(mc.get_path('dir_path_test'))
print(mc.get_path('dir_path_test2'))

mc.create_name(name_base='source', name_key='src', only_base=True)
mc.create_path_dir(dir_path=os.getcwd(), case_name=mc.get_name('src'), path_key='src')
mc.create_name(name_base='dist', name_key='dist', only_base=True)
mc.create_path_dir(dir_path=os.getcwd(), case_name=mc.get_name('dist'), path_key='dist')

mc.create_folder(directory=mc.get_path('dir'), folder_name='source', rewrite=True)

#mc.duplicate_case(src_path=mc.get_path('src'), dist_path=mc.get_path('dist'), make_new=True)
mc.duplicate_case(src_path=mc.get_path('src'), dist_path=mc.get_path('dist'), mode='rewrite')
mc.duplicate_case(src_path=mc.get_path('src'), dist_path=mc.get_path('dist'), mode='copy')

if __name__ == "__main__":
    main()
