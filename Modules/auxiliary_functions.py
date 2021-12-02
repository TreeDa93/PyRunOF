import os
import sys
import shutil
import traceback
from typing import List, Optional, Dict


class Files:
    """
    The class is intended to fulfill a number operations on files, for example, changing text ...

    Note:
        Probably, it is possible problems with coding for OS Windows

    Attributes
        ----------
    Methods
        -------
        change_text(self, dist_var, sour_var, name_file='')
             is the method to find and replace required text part at given file

        change_text_line(var_value, var_name, var_excl_name, path_dict=None, file_name='')
            The method fulfills row searching of the given variable var_name to change it to var_value
            if in the line there are not variable named as var_excl_name
    """

    def __init__(self):
        pass

    @staticmethod
    def change_var_fun(dist_var: str, sour_var: any, path: str = None, file_name: str = '') -> None:
        """Function to find and replace required text part at given file
            Attributes:
                 --------------
                dist_var is the depicts finding variables
                sour_var depicts replacing variables
                file_name is the name of file where the procedure will be done

        """
        path = os.path.join(path, file_name)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                old_data = f.read()
            new_data = old_data.replace(str(dist_var), str(sour_var))
            with open(path, 'w') as f:
                f.write(new_data)
        else:
            print(f'Warning: The file {file_name} is not exist!')

    @staticmethod
    def change_text_line(var_value: any, var_name: any, var_excl_name: any,
                         path: str = None, file_name: str = '') -> None:
        """ The function is served to find the variable named var_name in th file_name
        which has directory path_dict. If the variable has been founded and
        variable var_excl_name does not exist in the line then the value of the variable
        is changed by var_value
        Attributes:
        --------------
                var_value [string or numbers] is the value to be written instead var_name

                var_name depicts place in the given file where should be written var_value

                var_excl_name is the name to be absented in the text line in order to change founded variable var_name.

                path_dict is the path_dict with the required file for searching of given variable.

                file_name is the name of the file  where the method will fulfil searching.
        """
        path = os.path.join(path, file_name)
        new_data = ''
        with open(path, 'r') as f1:
            for line in f1:
                if (var_name in line) and (var_excl_name not in line):
                    new_line = f'{var_name} \t\t {var_value}; \n'
                    new_data += new_line
                    print(new_line)
                else:
                    new_data+=line
        with open(path, 'w') as f:
            f.write(new_data)


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

    def variable(self, var, key, where):
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
                if where[key] is not None:
                    return where[key]
                else:
                    self._raise_error(type_error='var_1')
            else:
                if where is not None:
                    return where
                else:
                    self._raise_error(type_error='var_2')
        else:
            return var

    def path_dict(self, path, path_key, where):
        """The method is intended to priority between the sent path_dict in the executing method and
            its object attributes of paths.
            Input :
                path_dict is the evaluating path_dict if the path_dict is None then
                path_key is the key of the dictionary storing value of required variable
                where: dict is the object where the method will be finding required variable by key
            Output:
                return var according priority
            Notice: The method is working only for dictionaries objects. If you need find second priority
                    in no dictionary object and as just variables you can use path method.
        """
        if path is None:
            if where[path_key] is not None:
                return where[path_key]
            else:
                self._raise_error(type_error='path_error')
        else:
            return path

    def path(self, path, path_key, where):
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
        if path is None:
            if type(where) is dict:
                if path[path_key] is not None:
                    return path[path_key]
                else:
                    self._raise_error(type_error='path_error')
            else:
                if where is not None:
                    return where
                else:
                    self._raise_error(type_error='path_error')
        else:
            return path

    def name(self, name, name_key, where):
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
            if where[name_key] is not None:
                return where[name_key]
            else:
                self._raise_error(type_error='name_error')
        else:
            return name

    def check_key(self, key, where):
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
            self._raise_error(key, type_error='check_key_error')

    def check_name(self, name, where):
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
            self._raise_error(name, type_error='check_name_error')

    def check_key_path(self, path, key, where):
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
                self._raise_error(type_error='check_key_path_error')
            else:
                return where[key]
        else:
            return path

    def check_key_name(self, name, key, where):
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
                self._raise_error(type_error='check_key_name_error')
            else:
                return where[key]
        else:
            return name

    def check_path_existence(self, check_path, make_new=False):
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
        if os.path.exists(check_path):
            return check_path
        else:
            dir_path, case_name = os.path.split(check_path)
            if os.path.exists(dir_path):
                if make_new is True:
                    os.mkdir(case_name)
                    return check_path
                else:
                    self._raise_error(check_path, dir_path, case_name, type_error='check_path_existence_error_1')
            else:
                self._raise_error(dir_path, case_name, type_error='check_path_existence_error_2')

    def check_path_existence_only(self, check_path):
        """The method checks existing of given path.
        #FIXME : improve description
        Input:
            check_path is the checking path
        Output:
            If the path exist the method return full
            if there is only directory of the final folder the method return 'dir'
        """

        if os.path.exists(check_path):
            return 'full'
        else:
            dir_path, case_name = os.path.split(check_path)
            if os.path.exists(dir_path):
                return 'dir'
            else:
                self._raise_error(dir_path, case_name, type_error='check_path_existence_error_2')

    def file(self, file):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if file is None:
            if self.file is not None:
                return self.file
            else:
                sys.exit('Error: You do not enter the name of the sif file!!!')
        else:
            return file

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

    @staticmethod
    def cores(core_OF, where):
        if core_OF is None:
            if where is not None:
                return where
            else:
                sys.exit('You have to set numbers of cores for OpenFOAM')
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
                sys.exit('Error: You do not enter the name of the sif file!!!')
        else:
            pass

    @staticmethod
    def _raise_error(*vargs, type_error=0):
        if type_error == 'var_1':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'var_2':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'path_error':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify path_dict either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'name_error':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify name either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'check_key_error':
            error_message = f''' 
                            ------------------------------------------
                            You write wrong key {vargs[0]}. Please check it.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'check_name_error':
            error_message = f''' 
                            ------------------------------------------
                            You write wrong name {vargs[0]}. Please check it.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'check_key_path':
            error_message = f''' 
                            ------------------------------------------
                            You have set neither the name nor the key to the name. 
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''

        elif type_error == 'check_path_existence_error_1':
            error_message = f''' 
                                ------------------------------------------
                                Your name {vargs[0]} and is not exist! But directory 
                                {vargs[1]} is exist! You can create folder {vargs[2]} 
                                yourself or set flag make_new as True to make the Folder
                                by the script with name {vargs[2]}! 
                                Above information can help you find where is it.
                                ------------------------------------------
                                '''
        elif type_error == 'check_path_existence_error_2':
            error_message = f''' 
                            ------------------------------------------
                            The given name is not exist and directory {vargs[0]}
                            of the folder {vargs[1]} is not exist as well.  
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        elif type_error == 'check_key_name_error':
            error_message = f''' 
                            ------------------------------------------
                            You have set neither the name nor the key to the name. 
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        else:
            error_message = f''' 
                            ------------------------------------------
                            YI do not know the error! The developer should it check!
                            ------------------------------------------
                            '''

        print(repr(traceback.format_stack()))
        raise SystemExit(error_message)

    @staticmethod
    def error_create_folder():
        error_message = f''' 
            ------------------------------------------
            The folder is already exist and your moder 
            of writing is available to make copy.
            Above information can help you find where is it.
            ------------------------------------------
            '''
        print(repr(traceback.format_stack()))
        raise SystemExit(error_message)

def copy_fun(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def copy_files(root_src_dir, root_dst_dir):
    for file_ in os.listdir(root_src_dir):
        src_file = os.path.join(root_src_dir, file_)
        dst_file = os.path.join(root_dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_file)


def copy_file(root_src_dir, root_dst_dir, nameFilesOld='', nameFileNew=''):
    src_file = os.path.join(root_src_dir, nameFilesOld)
    dst_file = os.path.join(root_dst_dir, nameFileNew)
    shutil.copy2(src_file, dst_file)