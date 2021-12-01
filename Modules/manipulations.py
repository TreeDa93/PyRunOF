import os
import sys
import shutil
import datetime
from typing import List, Optional, Dict
from Modules.auxiliary_functions import Priority


class Manipulations:
    """
    This class is designed to perform operations on case folders.
    attributes:
    paths is the dictionary consist of paths
    case_names is the dictionary of names of cases

    run_path is the system_path for key 'run
    new_path is
    name is the name of the class

    methods:
    duplicate_case is the function make copy or duplicate ot existing folder
    create_name is the function to create new name of case in self.case_names
    create_path_dir is the function creating system_path from director and folder
                        name in self.paths
    create_path is the method to create new system_path in self.paths
    change_path is the function serving to change existing system_path in self.system_path
    get_path is the function to get system_path by key
    get_name is the function to get name by key
    create_folder is function create new folder
    """

    def __init__(self,
                 name='test',
                 run_path: Optional[str] = None,
                 new_path: Optional[str] = None,
                 base_path: Optional[str] = None,
                 dir_path: Optional[str] = None, ):
        self.name = name
        self.paths = {'new': new_path,
                      'base': base_path,
                      'run': run_path,
                      'dir': dir_path}
        self.case_names = {'new': None,
                            'base': None,
                            'run': None}

    def __repr__(self):
        return f"Name of manipulation node ({self.name}, run name {self.paths['run']}, base name " \
               f"{self.paths['base']}, new name {self.paths['new']})"

    def __str__(self):
        return f"Name of manipulation node ({self.name}, runpath {self.paths['run']}, basepath " \
               f"{self.paths['base']}, newPath {self.paths['new']})"

    def duplicate_case(self,
                       src_path: Optional[str] = None,
                       dist_path: Optional[str] = None,
                       src_key: Optional[str] = None,
                       dist_key: Optional[str] = None,
                       mode: str = 'copy') -> None:
        """The function creates copy of the base case.
           pathBaseCase is the name of base case that will be copied by the function
           pathNewCase is the name of new case that will be created by the function
           mode defines how the procedure of copying will be done.
                   a) rewrite mode is the mode when folder of new case already being existed, then the folder
                   will delited by the function and base case folder will be copied to the folder being the same name
                   b) copy mode is the mode when folder of new case already being existed, then the folder will be copied
                   to the folder being old name with prefix of current time of copying. And new case will be copied
                    to folder being name of pathNewCase variables."""

        src_path = Priority.check_key_path(src_path, src_key, self.paths)
        dist_path = Priority.check_key_path(dist_path, dist_key, self.paths)
        Priority.check_path_existence(src_path, make_new=False)

        if mode == 'rewrite':
            if Priority.check_path_existence_only(dist_path) is 'full':
                shutil.rmtree(dist_path)
            shutil.copytree(src_path, dist_path)
        elif mode == 'copy':
            if Priority.check_path_existence_only(dist_path) is 'full':
                now = datetime.datetime.now()
                old_file = dist_path + '_' + 'old' + '_' + now.strftime("%d-%m-%Y %H:%M:%S")
                try:
                    shutil.move(dist_path, old_file)
                except shutil.Error:
                    print('You run the script is often. There is exception old case')
                shutil.copytree(src_path, dist_path)
            else:
                shutil.copytree(src_path, dist_path)

    def create_name(self, *case_names: List[str],
                    name_base: str = '',
                    name_key: Optional[str] = 'new',
                    splitter: Optional[str] = '_',
                    only_base: Optional[bool] = False) -> str:
        """The function serves to create two variables of base and new case paths.
        The name of new case is generated by special algorithm realized in the fucntion.
        The name will be created by adding variables of the list namesNewCase to base case folder name. The variables
        will be seprated by special sympol (spliter) to name of the folder.
         Variables:
                    *namesNewCase is a number of variables, which will be added to name of new case
                    baseCase is the folder name of base case
                splitter is the variables defending the for separation in folder name of new case
                only_base is the flat to crete name using only base part of name.

                """
        if only_base is True:
            self.case_names[name_key] = name_base
            return name_base
        else:
            for addName in case_names:
                name_base += splitter + str(addName)

            self.case_names[name_key] = name_base
            return self.case_names[name_key]

    def create_path_dir(self, dir_path: Optional[str] = None,
                        dir_path_key: Optional[str] = 'dir',
                        case_name: Optional[str] = None,
                        name_key: Optional[str] = None,
                        path_key: Optional[str] = 'new') -> str:
        """The function creates the name using directory and name of case
        Variables
        dirname is the name of directory where new folder of case put
        newCaseName is the name of new case

        newPath is the name of new case
        """
        cur_path = Priority.path(dir_path, dir_path_key, self.paths)
        cur_name = Priority.name(case_name, name_key, self.case_names)
        self.paths[path_key] = os.path.join(cur_path, cur_name)
        return self.paths[path_key]

    def create_path(self, path, path_key='testPath'):
        """The function is used to create your own name
        The created name will be written into dictionary self.addtionaldictionary with key  = name
        Input name is name of your new given name
        name is the key of dictionary storaged all addtional pathes"""
        self.paths[path_key] = path

    def change_path(self, new_path: str, path_key: str = 'newPath') -> None:
        """The function is used for changing existent name by name
        Input variables
        name is new given name
        key is the name of variables of key for dictionary of addtionals pathes"""
        if path_key in self.paths.keys():
            self.paths[path_key] = new_path
        else:
            print('Error the key of name is not exist!')

    def get_path(self, path_key: str) -> str:
        """The methods gives back name acording givven name or key
        Input:
        key is the name of class variables consisting pathes or key of dictionary with pathes """

        Priority.check_key(path_key, self.paths)
        return self.paths[path_key]

    def get_name(self, name_key: str) -> str:
        """The methods gives back name acording givven name or key
        Input:
        key is the name of class variables consisting pathes or key of dictionary with pathes """
        Priority.check_key(name_key, self.case_names)
        return self.case_names[name_key]

    def create_folder(self, directory: Optional[str] = None,
                      dir_key: Optional[str] = None,
                      folder_name: Optional[str] = None,
                      name_key: Optional[str] = None,
                      rewrite: Optional[bool] = True) -> None:
        """ The function is designed to create new folder
        :param directory:
        :param dir_key:
        :param folder_name:
        :param name_key:
        :param rewrite:
        :return:
        """

        directory = Priority.check_key_path(directory, dir_key, self.paths)
        folder_name = Priority.check_key_name(folder_name, name_key, self.case_names)

        full_path = os.path.join(directory, folder_name)
        test = Priority.check_path_existence_only(full_path)
        if test is 'full':
            if rewrite is True:
                shutil.rmtree(full_path)
                os.mkdir(full_path)
            else:
                Priority.error_create_folder()
        else:
            os.mkdir(full_path)
