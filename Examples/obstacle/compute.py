import sys
import os
from Modules.manipulations import Manipulations

libpath = '/home/ivan/PyRunOF/'
sys.path.append(libpath)
################
###Parameters###
################
src_case = 'obstacle_base'
src_name_key = 'src_name'
src_path_key = 'src_path'
dst_name_key = 'dst_name'

############


def main():
    mp = Manipulations(dir_path=os.getcwd())
    mp.create_name(name_base=src_case, name_key=src_name_key)
    mp.create_path_dir(dir_path_key='dir', name_key=src_name_key, path_key=src_path_key)
    mp.create_name('test', name_base=src_case, name_key=dst_name_key)
    mp.create_path_dir(dir_path_key='dir', name_key=dst_name_key)


if __name__ is '__main__':
    main()
