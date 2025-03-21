import sys
import shutil
import traceback
import pathlib as pl
import os
import json
from typing import Any
import subprocess
from typing import Sequence, Hashable
from .warning import raise_waring_files


def run_command(command: str, run_path):

    path_bash = pl.Path(__file__).parents[1] / 'files' / 'bash' / 'interactive_bash'

    if Files.is_executable(path_bash):
        subprocess.run(command, shell=True, executable=path_bash, cwd=run_path, start_new_session=True)
    else:
        subprocess.run(f'chmod +x {path_bash}', shell=True)

        subprocess.run(command, shell=True, executable=path_bash, cwd=run_path, start_new_session=True)

def merge_dicts(args: Sequence[dict]):
    dct = {}
    for entry in args:
        dct.update(entry)
    return dct

class Files:
    """
    The class is intended to fulfill a number of operations on files, for example, changing text ...

    Note:
        Probably, it is possible problems with coding for OS Windows

    Attributes
        ----------
    Methods
        -------
        change_var_fun is the method to find and replace required text part at given file

        change_text(cls, name_var, value_var, name_file='')
             is the method to find and replace required text part at given file

        change_text_line(var_value, var_name, var_excl_name, path_dict=None, file_name='')
            The method fulfills row searching of the given variable var_name to change it to var_value
            if in the line there are not variable named as var_excl_name
        copy_file is the method to make copy of a file and to move it to new path with new name.
        find_files is
        find_path_by_name
    """

    def __init__(self):
        pass

    @staticmethod
    def change_var_fun(name_var: str, value_var: any, path, file_name) -> None:
        """The function supports finding and replacing required text part at given file
        
        Arguments:
            * name_var depicts  require variable to be replaced
            * value_var depicts value to be inserted
            * path is the path of folder with file to be processed
            * file_name is the name of file where the procedure will be done
        
        Return: None
        """
        path = pl.Path(path) / file_name
        if path.is_file():
            with path.open(mode='r') as f:
                new_data = f.read().replace(str(name_var), str(value_var))
            with path.open(mode='w') as f:
                f.write(new_data)
        else:
            print(f'Warning: The file {file_name} is not exist!')

    @staticmethod
    def copy_file(root_src_dir, root_dst_dir, old_name, new_name):
        """The method make copy of a file and move it to new path with new name.
        Attributes:

        * root_src_dir [str or PathLike] is path of directory consisting of  file required for copy
        * root_dst_dir [str or PathLike] is the path of directory intended for new file
        * old_name [str] is the name of copying file
        * new_name [str] is the name of new copied file
        
        Return: None
        """

        src_file_path = pl.Path(root_src_dir)/old_name  # -> src_file = os.path.join(root_src_dir, old_name)
        dst_file_path = pl.Path(root_dst_dir)/new_name  # -> dst_file = os.path.join(root_dst_dir, new_name)
        shutil.copy2(src_file_path, dst_file_path)

    @staticmethod
    def find_files(where, type_files='file') -> list:
        """The method is intended to find all files at given directory and to sort by type file or directory.
        Attributes:
            -------------
        where is the path in which the method will find files or directories
        type_files is depicted type of finding files. It must be 'file' or 'directory'.
        Out:
            None
        """
        dirs = pl.Path(where).iterdir()
        if type_files == 'file':
            file_list = [file for file in dirs if file.is_file()]
            return file_list
        elif type_files == 'directory':
            dir_list = [cur_dir for cur_dir in dirs if cur_dir.is_dir()]
            return dir_list
        else:
            return list(dirs)
        
    @staticmethod
    def find_folders_by_word(
        word: str,
        directory: pl.Path
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

    @classmethod
    def find_path_by_name(cls, where, **options):
        """The method selects names from found list of names by comparing with required names in names.
        Attributes:
        -------------
            where is the path in which the method will find files or directories
            options:
                names [list] is the list of names by providing sort procedure.
        Out:
            None
        """
        dirs = cls.find_files(where, type_files='file')
        if options.get('file_names') is None:
            return dirs
        else:
            return [path for path in dirs if path.stem in options.get('file_names')]

    @staticmethod
    def open_json(file_path: str) -> dict:
        """Function to load json file content
            Attributes:
                 --------------
                file_path full path to json file
            Returns:
                 --------------
                dictionary with json file content
        """
        with open(file_path) as file:
            content = json.load(file)
        return content

    @staticmethod
    def save_json(data, save_path: str) -> None:
        """Function to save python dictionary as json file
            Attributes:
                 --------------
                data python dictionary with data
                file_path full path to json file
        """
        with open(save_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def is_executable(file_path):
        # Using shutil.which() to get the executable path
        executable_path = shutil.which(file_path)

        # Check if the executable path is not None and is executable
        if executable_path and os.access(executable_path, os.X_OK):
            return True
        else:
            return False
        
    @staticmethod
    def merge_dicts(args: Sequence[dict]):
        dct = {}
        for entry in args:
            dct.update(entry)
        return dct
    
    
class Priority:
    """
    The class is designed to choose priority between the sent variable in the executing method and
    its object attributes. The general sense of priority choosing is firstly to check the given variable in
    executing method, if the variable is None then to check the variable in the attributes of the object serving for
    execution of the method.

    Note:
        ---
        In the current version there are attributes. Their appointment is doubtful because highly likely
        the attribute will be deleted in the future.

    Attributes
        ----------
        paths is the dictionary of paths
        name_case is the dictionary of names
        sif_name is the name of elmer file with sif extension
        file is the name of file

    Methods
        -------
        variable(var, key, where)
        path_dict(path_dict, path_key, where)
        path(path_dict, path_key, where)
        name(name, name_key, where)
        check_key(key, where)
        check_name(name, where)
        check_key_path(path_dict, key, where)
        check_key_name
        check_path_existence
        check_path_existence_only
        error_create_folder
    """

    def __init__(self, names_cases: str = None, paths: str = None, sif_name: str = '.sif', file: str = None) -> None:
        self.paths = paths
        self.names_cases = names_cases
        self.sif_name = sif_name
        self.file = file

    @classmethod
    def variable(cls, var, where, var_key=None):
        """The method is intended to priority between the sent variable in the executing method and
            its object attributes.
            Input :
                var is the evaluating variable if the var is None then
                key is the key of the dictionary storing value of required variable
                where is the object where the method will be finding required variable by key
            Output:
                return var according priority
        """

        if var is None:
            if type(where) is dict:
                if var_key in where.keys():
                    if where[var_key] is None:
                        cls._raise_error(type_error='var_1')
                    else:
                        return where[var_key]
                else:
                    cls._raise_error(type_error='var_1')
            else:
                if where is None:
                    cls._raise_error(type_error='var_1')
                else:
                    return where
        else:
            return var

    @classmethod
    def path(cls, path, where, path_key=None):
        """The method is intended to priority between the sent path_dict in the executing method and
            its object attributes of paths.
            Input :
                path_dict is the evaluating path_dict if the path_dict is None then
                path_key is the key of the dictionary storing value of required variable
                where: dict is the object where the method will be finding required variable by key
            Output:
                return var according priority
            Notice: The method is working as with dictionaries and so variables.
        """
        if Priority._check_path_type(path):
            return pl.Path(path)
        elif path is None:
            if type(where) is dict:
                if path_key in where.keys():
                    if Priority._check_path_type(where[path_key]):
                        return pl.Path(where[path_key])
                    else:
    
                        cls._raise_error(type_error='path_error')
                else:
                    cls._raise_error(type_error='path_error')
            else:
                if Priority._check_path_type(where):
                    return pl.Path(where)
                else:
                    cls._raise_error(type_error='path_error')
        else:
            cls._raise_error(type_error='path_error')


    @classmethod
    def name(cls, name, where, name_key=None):
        """The method is used for selection of given name the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
            name is the checking name
            name_key is the key of the dictionary storing value of required name
            where is the object where the method will be finding required name by key
        Output:
            return name according priority
        """
        if name is None:
            if type(where) is dict:
                if name_key in where.keys():
                    if type(where[name_key]) is str:
                        return where[name_key]
                    else:
                        cls._raise_error(type_error='name_error')
                else:
                    cls._raise_error(type_error='name_error')
            elif type(where) is str:
                return where
            else:
                cls._raise_error(type_error='name_error')
        else:
            return name


    @classmethod
    def check_path_existence(cls, check_path, make_new=False):
        """The method is used for checking existing of given path.
        The method can check one lower level of the path as directory for existing if the directory is existent
        you can create new folder of your path by changing flag mane_new on True.
        FIXME : improve description
        Input :
             check_path is checking path
             make_new is logical variable to define crate new folder if directory of the file exist.

        Output:
            return path or error
        """
        check_path = pl.Path(check_path)
        if check_path.exists(): #  os.path.exists(check_path):
            return check_path
        else:
            #dir_path, case_name = os.path.split(check_path)
            if check_path.parent.exists():  # -> os.path.exists(dir_path):
                if make_new is True:
                    check_path.parent.mkdir(check_path.stem)  # -> os.mkdir(check_path.stem)
                    return check_path
                else:
                    cls._raise_error(check_path, check_path.parent, check_path.stem,
                                     type_error='check_path_existence_error_1')
            else:
                cls._raise_error(check_path.parent, check_path.stem,
                                 type_error='check_path_existence_error_2')

    @classmethod
    def check_path_existence_only(cls, check_path):
        
        """Check the existence of a given path.

        Parameters:
        check_path (str or Path): The path to check.

        Returns:
        str: 'full' if the path exists, 
        'dir' if only the parent directory of the final folder exists.
        'noExist' if the specify directory is not exist

        """
        check_path = pl.Path(check_path)
        if check_path.exists():  # ->os.path.exists(check_path):
            return 'full'
        elif check_path.parent.exists():  # -> os.path.exists(check_path.parent)
            return 'dir'
        else:
            return 'noExist'
            # cls._raise_error(check_path.parent, check_path.stem, type_error='check_path_existence_error_2')


    def sif_file(self, sif_file):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if sif_file is None:
            if self.sif_file is not None:
                return self.sif_file
            else:
                sys.exit('Error: You do not enter the name of the sif file!!!')
        else:
            return sif_file

    @classmethod
    def cores(cls, core_OF, where):
        if core_OF is None:
            if where is not None:
                return where
            else:
                cls._raise_error_run()
        else:
            return core_OF

    def _priority(self, var, type_priority='core'):
        """
        Test priority fun
        :param var:
        :return:
        """
        if var is None:
            return self._chose_type_priority(self, type_priority)
        else:
            return var

    def _chose_type_priority(self, type_priority):
        """The function defines priority between attribute variable
        and input variable of the executing method

        Input :
        type_priority is the flag to define for which variables to detirmine the priority
        Now it is avaible following flags
            * core_OF is core OpenFOAM flags
            * file is the file flag
        Output:
        attribute of the required variable or
        error that the required variables was not set

        """
        if type_priority == 'core_OF':
            if self.core_OF is not None:
                return self.core_OF
            else:
                sys.exit('You have to set numbers of cores for OpenFOAM')
        elif type_priority == 'file':
            if self.file is not None:
                return self.file
            else:
                sys.exit('Error: You do not enter the name of the file!!!')
        else:
            pass

    @staticmethod
    def _check_path_type(path) -> Any:
        """
        The function checks belonging of input variable to
        path is the checking variable
        return True or False
        """
        return type(path) in [str, os.PathLike, pl.PosixPath, pl.WindowsPath, pl.Path]


    @staticmethod
    def error_create_folder():
        error_message = f''' 
            ------------------------------------------
            The folder is already exist and your moder 
            of writing is available to make copy.
            Above information can help you find where is it.
            ------------------------------------------
            '''
        for message in traceback.format_stack():
            print(message)
        #print(repr(traceback.format_stack()))
        raise SystemExit(error_message)

    @staticmethod
    def _raise_error_run():
        sys.exit('You have to set numbers of cores for OpenFOAM')

