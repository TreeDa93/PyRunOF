import shutil
import pathlib as pl
from time import strftime, sleep
from typing import List, Optional, Dict
from Modules.auxiliary_functions import Priority, Files
from Modules.information import Information


class Manipulations(Information):
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
    create_name is the function to create new name of case in cls.case_names
    create_path_dir is the function creating system_path from director and folder
                        name in cls.paths
    create_path is the method to create new system_path in cls.paths
    change_path is the function serving to change existing system_path in cls.system_path
    get_path is the function to get system_path by key
    get_name is the function to get name by key
    create_folder is function create new folder
    """

    def __init__(self, info_key: Optional[str] = 'general',
                 name='test',
                 run_path: Optional[str] = None,
                 new_path: Optional[str] = None,
                 base_path: Optional[str] = None,
                 dir_path: Optional[str] = None, ):

        Information.__init_manipulation__(self, info_key=info_key,
                                          name=name,
                                          run_path=run_path,
                                          new_path=new_path,
                                          base_path=base_path,
                                          dir_path=dir_path, )

    def __repr__(self):
        return f"Name of manipulation node ({self.info[self.info_key]['name']}, run name {self.info[self.info_key]['paths']['run']}, " \
               f"base name " \
               f"{self.info[self.info_key]['paths']['base']}, new name {self.info[self.info_key]['paths']['new']})"

    def __str__(self):
        return f"Name of manipulation node ({self.info[self.info_key]['name']}, runpath {self.info[self.info_key]['paths']['run']}, basepath " \
               f"{self.info[self.info_key]['paths']['base']}, newPath {self.info[self.info_key]['paths']['new']})"

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
                   b) copy mode is the mode when folder of new case already being existed, then the folder
                   will be copied
                   to the folder being old name with prefix of current time of copying. And new case will be copied
                    to folder being name of pathNewCase variables."""

        src_path = pl.Path(Priority.check_key_path(src_path, src_key, self.info[self.info_key]['paths']))
        dist_path = pl.Path(Priority.check_key_path(dist_path, dist_key, self.info[self.info_key]['paths']))
        Priority.check_path_existence(src_path, make_new=False)

        if mode == 'rewrite':
            if Priority.check_path_existence_only(dist_path) == 'full':
                shutil.rmtree(dist_path)
            shutil.copytree(src_path, dist_path)
        elif mode == 'copy':
            if Priority.check_path_existence_only(dist_path) == 'full':
                old_name = dist_path.stem + '_' + 'old' + '_' + strftime('%d-%m-%Y %H-%M')
                old_path = dist_path.parent / old_name
                if old_path.exists():
                    sleep(1)
                    old_name = dist_path.stem + '_' + 'old' + '_' + strftime('%d-%m-%Y %H-%M-%S')
                    old_path = dist_path.parent / old_name
                    dist_path.replace(old_path)
                else:
                    dist_path.replace(old_path)
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
            self.info[self.info_key]['case_names'][name_key] = name_base
            return name_base
        else:
            for addName in case_names:
                name_base += splitter + str(addName)

            self.info[self.info_key]['case_names'][name_key] = name_base
            return self.info[self.info_key]['case_names'][name_key]

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
        cur_path = Priority.path(dir_path, self.info[self.info_key]['paths'], path_key=dir_path_key)
        cur_name = Priority.name(case_name, self.info[self.info_key]['case_names'], name_key=name_key)
        self.info[self.info_key]['paths'][path_key] = pl.Path(cur_path) / cur_name
        return self.info[self.info_key]['paths'][path_key]

    def create_path(self, path, path_key='testPath'):
        """The function is used to create your own name
        The created name will be written into dictionary cls.addtionaldictionary with key  = name
        Input name is name of your new given name
        name is the key of dictionary storaged all addtional pathes"""
        self.info[self.info_key]['paths'][path_key] = path

    def change_path(self, new_path: str, path_key: str = 'newPath') -> None:
        """The function is used for changing existent name by name
        Input variables
        name is new given name
        key is the name of variables of key for dictionary of addtionals pathes"""
        if path_key in self.info[self.info_key]['paths'].keys():
            self.info[self.info_key]['paths'][path_key] = new_path
        else:
            print('Error the key of name is not exist!')

    def get_name(self, name_key: str) -> str:
        """The method returns the name according given key
        Input:
        key is the name of class variables consisting pathes or key of dictionary with pathes """
        Priority.check_key(name_key, self.info[self.info_key]['case_names'])
        return self.info[self.info_key]['case_names'][name_key]

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

        directory = Priority.check_key_path(directory, dir_key, self.info[self.info_key]['paths'])
        folder_name = Priority.check_key_name(folder_name, name_key, self.info[self.info_key]['case_names'])

        full_path = pl.Path(directory) / folder_name
        test = Priority.check_path_existence_only(full_path)
        if test == 'full':
            if rewrite is True:
                shutil.rmtree(full_path)
                full_path.mkdir()
            else:
                Priority.error_create_folder()
        else:
            full_path.mkdir()

    def delete_case(self, full_path: Optional[str] = None,
                    dir_key: Optional[str] = None,
                    directory: Optional[str] = None,
                    folder_name: Optional[str] = None,
                    name_key: Optional[str] = None,
                    ) -> None:
        """ The function is designed to delete a case
                :param full_path:
                :param dir_key:
                :param directory:
                :param folder_name:
                :param name_key:
                :return:
                """
        if full_path is None:
            print('I am here!!!!')
            directory = Priority.check_key_path(directory, dir_key, self.info[self.info_key]['paths'])
            folder_name = Priority.check_key_name(folder_name, name_key, self.info[self.info_key]['case_names'])
            full_path = pl.Path(directory) / folder_name
            test = Priority.check_path_existence_only(full_path)
            if test == 'full':
                shutil.rmtree(full_path)
            else:
                print(f'Warning: The directory ({full_path.parent}) is exist'
                      f'but the file to be deleted ({full_path.stem}) is missing!!!')
        else:
            full_path = pl.Path(full_path)
            if Priority.check_path_existence_only(full_path) == 'full':
                shutil.rmtree(full_path)
            else:
                print(f'Warning: The directory ({full_path.parent}) is exist'
                      f'but the file to be deleted ({full_path.stem}) is missing!!!')

    def delete_cases(self, full_pathes: Optional[list] = None,
                     words: Optional[list] = None, directory: Optional[str] = None,
                     dir_key: Optional[str] = None) -> None:
        """ The function is designed to delete a case
                :param full_path:
                :param dir_key:
                :param folder_name:
                :param name_key:
                :param rewrite:
                :return:
                """
        if full_pathes is not None:
            for full_path in full_pathes:
                full_path = pl.Path(full_path)
                if Priority.check_path_existence_only(full_path) == 'full':
                    shutil.rmtree(full_path)
                else:
                    print(f'Warning: The directory ({full_path.parent}) is exist'
                          f'but the file to be deleted ({full_path.stem}) is missing!!!')
        elif words is not None:
            for word in words:
                full_pathes, _ = self.find_folders_by_word(word=word, directory=directory, dir_key=dir_key)
                for full_path in full_pathes:
                    shutil.rmtree(full_path)
        else:
            print('ERROR: You have to enter or the list of full_pathes either'
                  'the list of words')

    def find_folders_by_word(self, word: [str], directory: Optional[str] = None,
                             dir_key: Optional[str] = None):
        directory = pl.Path(Priority.check_key_path(directory, dir_key, self.info[self.info_key]['paths']))
        full_find_path = [folder for folder in directory.iterdir() if word in folder.stem]
        name_find_file = [folder.stem for folder in directory.iterdir() if word in folder.stem]
        return full_find_path, name_find_file

    @staticmethod
    def change_json_params(parameters_path: Optional[str] = None, changed_parameters: Optional[dict] = None,
                           save_path: Optional[str] = None):
        parameters = Files.open_json(parameters_path)
        parameters.update(changed_parameters)
        if save_path is None:
            save_path = parameters_path
        Files.save_json(parameters, save_path)

    @staticmethod
    def create_json_params(*parameter_dict: dict, save_path: Optional[str] = None):
        collect_dict = dict()
        for dict_i in parameter_dict:
            collect_dict.update(dict_i)

        Files.save_json(collect_dict, save_path)

    @staticmethod
    def get_dict_from_json(parameters_path):
        return Files.open_json(parameters_path)



