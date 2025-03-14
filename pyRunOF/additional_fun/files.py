import pathlib as pl
import shutil
import os
import json
from typing import Sequence

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


def save_json(data, save_path: str) -> None:
    """Function to save python dictionary as json file
        Attributes:
                --------------
            data python dictionary with data
            file_path full path to json file
    """
    with open(save_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def is_executable(file_path):
    # Using shutil.which() to get the executable path
    executable_path = shutil.which(file_path)

    # Check if the executable path is not None and is executable
    if executable_path and os.access(executable_path, os.X_OK):
        return True
    else:
        return False
    

def merge_dicts(args: Sequence[dict]):
    dct = {}
    for entry in args:
        dct.update(entry)
    return dct