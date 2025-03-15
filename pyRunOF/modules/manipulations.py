import os
import shutil
import pathlib as pl
from time import strftime, sleep
from typing import Optional, Union

from ..additional_fun.auxiliary_functions import Priority, Files
from ..additional_fun.information import Information


class Manipulations(Information):
    """
    This class is designed to perform operations on case folders.
    attributes:
    paths is the dictionary consist of paths
    case_names is the dictionary of names of cases

    run_path is the system_path for key run
    new_path is
    name is the name of the class

    Methods:
    *   duplicate_case is the function make copy or duplicate ot existing folder
    *   create_name is the function to create new name of case in cls.case_names
    *   create_path_dir is the function creating system_path from director and folder
                        name in cls.paths
    *   create_path is the method to create new system_path in cls.paths
    *   change_path is the function serving to change existing system_path in cls.system_path
    *   get_path is the function to get system_path by key
    *   get_name is the function to get name by key
    *   create_folder is function create new folder
    """

    def __init__(self, **optional_args):
        """Initializes the manipulation with optional arguments.
            optional arguments:
                info_key (Optional[str]): The main key for the information dictionary. Defaults to 'general'.
                dir_path (Optional[str]): The directory path. Defaults to None.
                set_names (Optional[list]): A list of set names to initialize in the information dictionary. Defaults to ['paths', 'names'].
        Returns:
            None"""
    
        Information.__init_manipulation__(self, **optional_args)

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

    def create_folder(self, directory: Optional[str] = None,
                      dir_key: Optional[str] = None,
                      folder_name: Optional[str] = None,
                      name_key: Optional[str] = None,
                      rewrite: Optional[bool] = True,
                      info_key=None) -> None:
        """ The function is designed to create new folder
        :param directory:
        :param dir_key:
        :param folder_name:
        :param name_key:
        :param rewrite:
        :return:
        """
        info_key = self.get_key(info_key)
        directory = Priority.path(directory, self.info[info_key]['paths'], path_key=dir_key)
        folder_name = Priority.name(folder_name, self.info[info_key]['case_names'], name_key=name_key)

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

    def create_folder_by_path(self, path: Optional[str] = None,
                      path_key: Optional[str] = None,
                      rewrite: Optional[bool] = True) -> None:
        path = Priority.path(path, self.info[self.info_key]['paths'], path_key=path_key)
        test = Priority.check_path_existence_only(path)
        if test == 'full':
            if rewrite is True:
                shutil.rmtree(path)
                path.mkdir()
            else:
                Priority.error_create_folder()
        else:
            path.mkdir()

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
                    if full_path.is_file():
                        os.remove(full_path)
                    else:
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
    def change_json_params(parameters_path: str, changed_parameters: dict,
                           save_path: Union[str, pl.Path] = None):
        parameters = Files.open_json(parameters_path)
        parameters.update(changed_parameters)
        if save_path is None:
            save_path = parameters_path
        Files.save_json(parameters, save_path)

    @staticmethod
    def create_json_params(*parameter_dict: dict, save_path: Optional[str] = None):
        """
        The function creates new json file with parameters and save it in save_path.
        Args:
            *parameter_dict: a number of dictionaries consist of  parameter names as keys and values of parameters as
                                values of the key.
            save_path:      the path in which json file will save.

        Returns:

        """
        collect_dict = dict()
        for dict_i in parameter_dict:
            collect_dict.update(dict_i)

        Files.save_json(collect_dict, save_path)

    @staticmethod
    def get_dict_from_json(parameters_path):
        return Files.open_json(parameters_path)
    
    def __str__(self):
        representation_stirng = str()
        for key, val_info in self.info.items():
            representation_stirng += f'Information of {key} \n'
            for key, data in val_info.items():
                representation_stirng += f'{key} :\n'
                for sub_key, sub_data in data.items():
                    representation_stirng += f'{sub_key} : {sub_data}:\n'
        return representation_stirng

    def __repr__(self):
        representation_stirng = str()
        for key, val_info in self.info.items():
            representation_stirng += f'Information of {key} \n'
            for key, data in val_info.items():
                representation_stirng += f'{key} :\n'
                for sub_key, sub_data in data.items():
                    representation_stirng += f'{sub_key} : {sub_data}:\n'

        return representation_stirng