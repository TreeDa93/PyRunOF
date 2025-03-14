import sys
import shutil
import traceback
import pathlib as pl
import os
import json
from typing import Any
import subprocess


def variable(var, where, var_key=None):
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
def path_add_folder(cls, path, where, add_folder, path_key=None):
    path = cls.path(path, where, path_key=path_key)
    return pl.Path(path) / add_folder

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
def check_key(cls, key, where):
    """The method is used to check existence of the key in object named where
    If both key is not existence in where then program raise error!
    Input :
        key is checking key
        where is the object [dict] for checking
    Output:
        return pass or error
    """
    if key in where:
        pass
    else:
        cls._raise_error(key, type_error='check_key_error')

@classmethod
def check_name(cls, name, where):
    """The method is used to check existence of the name in object named where
    If both name is not existence in where then program raise error!
    Input :
            name is checking name
            where is the object [dict] for checking
    Output:
        return pass or error
    """
    if name in where:
        pass
    else:
        cls._raise_error(name, type_error='check_name_error')

@classmethod
def check_key_path(cls, path, key, where):
    """This method is used to check whether the path was specified in
        the method or there is this path in the attributes of the object where.
        If both case is False then the method raise error!
            Input :
                    path is checking path
                    key is the key of path which can be existed in where
                    where is the object [dict] for checking
            Output:
                return path or error
            """
    if path is None:
        if key is None:
            cls._raise_error(type_error='check_key_path_error')
        else:
            return where[key]
    else:
        return path

@classmethod
def check_key_name(cls, name, key, where):
    """This method is used to check whether the path was specified in
        the method or there is this path in the attributes of the object where.
        If both case is False then the method raise error!
            Input :
                    path is checking path
                    key is the key of path which can be existed in where
                    where is the object [dict] for checking
            Output:
                return path or error
            """
    if name is None:
        if key is None:
            cls._raise_error(type_error='check_key_name_error')
        else:
            return where[key]
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
            cls._raise_error(check_path.parent, check_path.stem, type_error='check_path_existence_error_2')


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
    return type(path) in [str, os.PathLike, pl.PosixPath, pl.WindowsPath]

