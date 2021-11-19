import sys # import library
import os
libpath = 'C:\\Users\\Ivan\\science\\works\\PyFoam\\PyRunOF' #write path to pyRunOF library
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

mc.create_name('test2', '1', '3', name_base='base1', name_key='test2')
mc.get_name('test2')

# test paths
mc.create_path_dir(case_name='disFolder', path_key='new')

mc.create_path_dir(dirname=os.getcwd(), case_name='disFolder', path_key='run')
mc.create_path_dir(dirname=os.getcwd(), case_name='srsFolder', path_key='base')
mc.create_path_dir(dirname=os.getcwd(), case_name='copyFolder', path_key='test2')
mc.create_path(os.path.join(os.getcwd(), 'copyFolder'), path_key='test2_2')
mc.get_path(path_key='test2')
mc.get_path(path_key='test2_2')
mc.get_path(path_key='test4')

#mc.get_path('newName')
#mc.dublicate_case()
if __name__ == "__main__":
    main()
