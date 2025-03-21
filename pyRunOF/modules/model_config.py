import os
import shutil
import pathlib as pl
from time import strftime, sleep
from typing import Optional, Union
from collections.abc import Iterable

from ..additional_fun.auxiliary_functions import Priority, Files
from ..additional_fun.information import Information
from ..additional_fun.warning import raise_waring_files

class ModelConfigurator(Information):
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

    def duplicate_case(
        self,
        src_path: Optional[str] = None,
        dist_path: Optional[str] = None,
        src_key: Optional[str] = None,
        dist_key: Optional[str] = None,
        mode: str = "copy",
    ) -> None:
        """Creates a copy of the base case.

        Args:
            src_path (Optional[str]): The source path of the base case to be copied.
            dist_path (Optional[str]): The destination path where the new case will be created.
                   will be deleted by the function and base case folder will be copied to the folder being the same name
            dist_key (Optional[str]): The key for the destination path in the paths dictionary.
            mode (str): Defines how the copying procedure will be done.
                        'rewrite' mode will delete the existing folder at the destination path and copy the base case folder to the new path.
                        'copy' mode will rename the existing folder at the destination path with a prefix of the current time and copy the base case folder to the destination path.

        Returns:
            None
        """
        print("\n info key:", self.info[self.info_key])

        src_path = pl.Path(
            Priority.check_key_path(
                src_path, src_key, self.info[self.info_key]["paths"]
            )
        )
        dist_path = pl.Path(
            Priority.check_key_path(
                dist_path, dist_key, self.info[self.info_key]["paths"]
            )
        )
        Priority.check_path_existence(src_path, make_new=False)
        if mode == "rewrite":
            if Priority.check_path_existence_only(dist_path) == "full":
                shutil.rmtree(dist_path)
            shutil.copytree(src_path, dist_path)
        elif mode == "copy":
            if Priority.check_path_existence_only(dist_path) == "full":
                old_name = (
                    dist_path.stem + "_" + "old" + "_" + strftime("%d-%m-%Y %H-%M")
                )
                old_path = dist_path.parent / old_name
                if old_path.exists():
                    sleep(1)
                    old_name = (
                        dist_path.stem
                        + "_"
                        + "old"
                        + "_"
                        + strftime("%d-%m-%Y %H-%M-%S")
                    )
                    old_path = dist_path.parent / old_name
                    dist_path.rename(old_path)
                else:
                    dist_path.replace(old_path)
                shutil.copytree(src_path, dist_path)
            else:
                shutil.copytree(src_path, dist_path)

    def create_folder(
        self,
        directory: Optional[str] = None,
        dir_key: Optional[str] = None,
        folder_name: Optional[str] = None,
        name_key: Optional[str] = None,
        rewrite: Optional[bool] = True,
        info_key=None,
    ) -> None:
        """Creates a new folder.

        Args:
            directory (Optional[str]): The directory path where the new folder will be created.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary.
            folder_name (Optional[str]): The name of the new folder to be created.
            name_key (Optional[str]): The key for the folder name in the case_names dictionary.
            rewrite (Optional[bool]): If True, the existing folder will be deleted and a new one will be created. Defaults to True.
            info_key (Optional[str]): The key for the information dictionary. Defaults to None.

        Returns:
            None
        """
        info_key = self.get_key(info_key)
        directory = Priority.path(
            directory, self.info[info_key]["paths"], path_key=dir_key
        )
        folder_name = Priority.name(
            folder_name, self.info[info_key]["case_names"], name_key=name_key
        )

        full_path = pl.Path(directory) / folder_name
        test = Priority.check_path_existence_only(full_path)
        if test == "full":
            if rewrite is True:
                shutil.rmtree(full_path)
                full_path.mkdir()
            else:
                Priority.error_create_folder()
        else:
            full_path.mkdir()

    def create_folder_by_path(
        self,
        path: Optional[str] = None,
        path_key: Optional[str] = None,
        rewrite: Optional[bool] = True,
    ) -> None:
        """Creates a new folder by the given path or path key.

        Args:
            path (Optional[str]): The path where the new folder will be created.
            path_key (Optional[str]): The key for the path in the paths dictionary.
            rewrite (Optional[bool]): If True, the existing folder will be deleted and a new one will be created. Defaults to True.

        Returns:
            None
        """
        path = Priority.path(path, self.info[self.info_key]["paths"], path_key=path_key)
        test = Priority.check_path_existence_only(path)
        if test == "full":
            if rewrite is True:
                shutil.rmtree(path)
                path.mkdir()
            else:
                Priority.error_create_folder()
        else:
            path.mkdir()

    def delete_folders_by_words(
        self,
        words: Iterable|str,
        directory: Optional[str] = None,
        dir_key: Optional[str] = None,
    ) -> None:
        if isinstance(words, Iterable) and not isinstance(words, str):
            for word in words:
                folder_paths = self.find_folders_by_word(word, directory=directory,
                                          dir_key=dir_key)
                self.delete_folders(folder_paths, directory=directory,
                                    dir_key=dir_key)
        else:
            folder_paths = self.find_folders_by_word(words, directory=directory,
                                          dir_key=dir_key)
            self.delete_folders(folder_paths, directory=directory,
                                dir_key=dir_key)

    def delete_folders(
        self,
        folders: Optional[list[str]] = None,
        directory: Optional[str] = None,
        dir_key: Optional[str] = None,
    ) -> None:
        """Deletes specified folders.

        Args:
            folders (Optional[list[str]]): A list of folder names to be deleted.
            directory (Optional[str]): The directory path where the folders are located.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary.

        Returns:
            None
        """

        directory = Priority.path(directory, self.info[self.info_key]["paths"], path_key=dir_key)
        
        for folder_name in folders:
            folder_path = pl.Path(directory) / folder_name
            if folder_path.exists() and folder_path.is_dir():
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")
            else:
                print(f"Folder not found: {folder_path}")

    def find_folders_by_word(
        self,
        word: str,
        directory: Optional[str] = None,
        dir_key: Optional[str] = None,
    ) -> tuple[list[pl.Path], list[str]]:
        """
        Finds folders in a directory that contain a specific word in their name.

        Args:
            word (str): The word to search for in folder names.
            directory (Optional[str]): The directory path to search in. Defaults to None.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary. Defaults to None.

        Returns:
            tuple: A tuple containing two lists:
                - full_find_path (list): List of full paths to folders containing the word.
                - name_find_file (list): List of folder names containing the word.
        """
        directory = pl.Path(
            Priority.check_key_path(
                directory, dir_key, self.info[self.info_key]["paths"]
            )
        )
        if not directory.exists():
            
            raise_waring_files('DIR_NOT_EXIST', directory=directory)
            
            return None
        elif isinstance(word, str):
            
            raise_waring_files('WORD_TYPE', directory=directory)
            
            return None

        full_find_path = [
            folder for folder in directory.iterdir() if word in folder.stem
        ]
        name_find_file = [
            folder.stem for folder in directory.iterdir() if word in folder.stem
        ]

        if full_find_path == []:

            raise_waring_files('NOTHING FOUND', directory=directory, word=word)
            
            return None
        else:
            return full_find_path, name_find_file

    @staticmethod
    def change_json_params(
        parameters_path: str,
        changed_parameters: dict,
        save_path: Union[str, pl.Path] = None,
    ):
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
            representation_stirng += f"Information of {key} \n"
            for key, data in val_info.items():
                representation_stirng += f"{key} :\n"
                for sub_key, sub_data in data.items():
                    representation_stirng += f"{sub_key} : {sub_data}:\n"
        return representation_stirng

    def __repr__(self):
        representation_stirng = str()
        for key, val_info in self.info.items():
            representation_stirng += f"Information of {key} \n"
            for key, data in val_info.items():
                representation_stirng += f"{key} :\n"
                for sub_key, sub_data in data.items():
                    representation_stirng += f"{sub_key} : {sub_data}:\n"

        return representation_stirng
