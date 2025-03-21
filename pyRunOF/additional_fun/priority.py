import pathlib as pl
import os
from typing import Any, Hashable
from .error import raise_error_priority as raise_error


def select_var(var, info_node, var_key):
    """The method is intended to priority between the sent variable in the executing method and
        its object attributes.
        Input :
            var is the evaluating variable if the var is None then
            key is the key of the dictionary storing value of required variable
            where is the object where the method will be finding required variable by key
        Output:
            return var according priority
    """
    return _select_req_input_args(var, info_node, var_key)


def select_path(path, info_node, path_key):
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

    path = _select_req_input_args(path, info_node, path_key)

    if _check_path_type(path):
        return pl.Path(path)
    else:
        raise_error('PATH:INCCORECT_PATH_TYPE')

def select_name(name, info_node, path_key):
    name = _select_req_input_args(name, info_node, path_key)

    if isinstance(name, str):
        return name
    else:
        raise_error('NAME:INCCORECT_TYPE', name_type=type(name))
    
def check_path_existence(check_path, make_new=False):
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
                raise_error('CHECK_PATH_EXIST_1', path=check_path, 
                            folder=check_path.stem, dir=check_path.parent)
        else:   
            raise_error('CHECK_PATH_EXIST_2', path=check_path, 
                        folder=check_path.stem, dir=check_path.parent)


def check_path_existence_only(check_path):
    """The method checks existing of given path.
    #FIXME : improve description
    Input:
        check_path is the checking path
    Output:
        If the path exist the method return full
        if there is only directory of the final folder the method return 'dir'
    """
    check_path = pl.Path(check_path)
    if check_path.exists():  # ->os.path.exists(check_path):
        return 'full'
    else:
        #dir_path, case_name = os.path.split(check_path)
        if check_path.parent.exists():  # -> os.path.exists(check_path.parent):
            return 'dir'
        else:
            raise_error('CHECK_PATH_EXIST_2', path=check_path, 
                        folder=check_path.stem, dir=check_path.parent)

def _select_req_input_args(*args, mode='default'):
    
    if mode == 'default':
        var, info_node, node_key = args
        if var is None:
            if _exist_dict_and_key(info_node, node_key):
                try:
                    _ = info_node[node_key]
                except KeyError:
                    raise_error('INFO:KEY_ERROR', info_node=info_node,
                                key=node_key)
                else:
                    return info_node[node_key]
            else:
                raise_error('PRIORITY:NO_CORRECT_ARGS', 
                            var=var,
                            )
        else:
            return var
    else:
        raise_error('INCORRECT_MODE_TO_SELECT', mode=mode)

def _exist_dict_and_key(info_node, node_key):
    
    return _check_type_info(info_node) and _check_type_info_key(node_key)


def _check_type_info_key(key):
    if key is not None and isinstance(key, Hashable):
        return True
    else:
         raise_error('INFO:INCORRECT_KEY_TYPE',
                     key=key,
                     key_type=type(key))

def _check_type_info(info_node):
    if isinstance(info_node, dict):
        return True
    else: 
        raise_error('INFO:IS_NOT_DICT', 
                    info=info_node, 
                    info_type=type(info_node))


def _check_path_type(path) -> Any:
    """
    The function checks belonging of input variable to
    path is the checking variable
    return True or False
    """
    path_types = (str, 
                  os.PathLike, 
                  pl.PosixPath, 
                  pl.WindowsPath
                  )
    
    return isinstance(path, path_types)

