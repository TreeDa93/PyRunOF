import os
import sys
import shutil
import traceback


class Files:
    """
    Discription of class
    FIXME
    Note:
        Возможны проблемы с кодировкой в Windows

    Attributes
        ----------
        file_path : str
            полный путь до текстового файла
        lines : list
            список строк исходного файла

    Methods
        -------
        change_text(self, dist_var, sour_var, name_file='')
            Разделяет строки списка по указанному разделителю
            и возвращает результат в виде списка
    """

    def __init__(self):
        pass

    @staticmethod
    def change_var_fun(dist_var, sour_var, path=None, file_name=''):
        """Function to find and replace required text part at given file
                dist_var is the depicts finding variables
                sour_var depicts replacing variables
                nameFile is the name of file where the procedure will be done

        """
        path = os.path.join(path, file_name)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                oldData = f.read()
            newData = oldData.replace(str(dist_var), str(sour_var))
            with open(path, 'w') as f:
                f.write(newData)
        else:
            print(f'Warning: The file {file_name} is not exist!')

    @staticmethod
    def change_text_line(var_value, var_name, var_excl_name, path=None, file_name=''):
        """ The function is served to find the variable named var_name in th file_name
        which has directory path. If the variable has been founded and
        variable var_excl_name does not exist in the line then the value of the variable
        is changed by var_value"""
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
    """The class is designed to chose priority between some objects

    """

    def __init__(self, names_cases=None, paths=None, sif_name='.sif', file=None):
        self.paths = paths
        self.names_cases = names_cases
        self.sifName = sif_name
        self.file = file

    @staticmethod
    def variable(var, key, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """

        if var is None:
            if type(where) is dict:
                if where[key] is not None:
                    return where[key]
                else:
                    error_message = f''' 
                    ------------------------------------------
                    You did not specify either in the object or 
                    in the method.
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                    print(repr(traceback.format_stack()))
                    raise SystemExit(error_message)
            else:
                if where is not None:
                    return where
                else:
                    error_message = f''' 
                    ------------------------------------------
                    You did not specify either in the object or 
                    in the method.
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                    print(repr(traceback.format_stack()))
                    raise SystemExit(error_message)
        else:
            return var

    @staticmethod
    def path(path_case, path_key, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if path_case is None:
            if where[path_key] is not None:
                return where[path_key]
            else:
                error_message = f''' 
                ------------------------------------------
                You did not specify either in the object or 
                in the method.
                Above information can help you find where is it.
                ------------------------------------------
                '''
                print(repr(traceback.format_stack()))
                raise SystemExit(error_message)
        else:
            return path_case
    @staticmethod
    def path2(path_case, path_key, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if path_case is None:
            if type(where) is dict:
                if path_case[path_key] is not None:
                    return path_case[path_key]
                else:
                    error_message = f''' 
                    ------------------------------------------
                    You did not specify either in the object or 
                    in the method.
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                    print(repr(traceback.format_stack()))
                    raise SystemExit(error_message)
            else:
                if where is not None:
                    return where
                else:
                    error_message = f''' 
                    ------------------------------------------
                    You did not specify either in the object or 
                    in the method.
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                    print(repr(traceback.format_stack()))
                    raise SystemExit(error_message)
        else:
            return path_case

    @staticmethod
    def name(name, name_key, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if name is None:
            if where[name_key] is not None:
                return where[name_key]
            else:
                error_message = f''' 
                ------------------------------------------
                You did not specify either in the object or 
                in the method.
                Above information can help you find where is it.
                ------------------------------------------
                '''
                print(repr(traceback.format_stack()))
                raise SystemExit(error_message)
        else:
            return name

    @staticmethod
    def check_key(key, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if key in where:
            pass
        else:
            error_message = f''' 
            ------------------------------------------
            You write wrong key {key}. Please check it.
            Above information can help you find where is it.
            ------------------------------------------
            '''
            print(repr(traceback.format_stack()))
            raise SystemExit(error_message)

    @staticmethod
    def check_name(name, where):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if name in where:
            pass
        else:
            error_message = f''' 
                ------------------------------------------
                You write wrong name {name}. Please check it.
                Above information can help you find where is it.
                ------------------------------------------
                '''
            print(repr(traceback.format_stack()))
            raise SystemExit(error_message)

    @staticmethod
    def check_key_path(path, key, where):
        if path is None:
            if key is None:
                error_message = f''' 
                ------------------------------------------
                You have set neither the name nor the key to the name. 
                Above information can help you find where is it.
                ------------------------------------------
                '''
                print(repr(traceback.format_stack()))
                raise SystemExit(error_message)
            else:
                return where[key]
        else:
            return path

    @staticmethod
    def check_key_name(name, key, where):
        if name is None:
            if key is None:
                error_message = f''' 
                    ------------------------------------------
                    You have set neither the name nor the key to the name. 
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                print(repr(traceback.format_stack()))
                raise SystemExit(error_message)
            else:
                return where[key]
        else:
            return name

    @staticmethod
    def check_path_existence(check_path, make_new=False):
        """The method supports to find out existing gotten pathes
        If one of the gotten pathes is not exist, program is interupted
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
                    error_message = f''' 
                    ------------------------------------------
                    Your name {check_path} and is not exist! But directory 
                    {dir_path} is exist! You can create folder {case_name} 
                    yourself or set flag make_new as True to make the Folder
                    by the script with name {case_name}! 
                    Above information can help you find where is it.
                    ------------------------------------------
                    '''
                    print(repr(traceback.format_stack()))
                    raise SystemExit(error_message)
            else:
                error_message = f''' 
                ------------------------------------------
                The given name is not exist and directory {dir_path}
                of the folder {case_name} is not exist as well.  
                Above information can help you find where is it.
                ------------------------------------------
                '''
                print(repr(traceback.format_stack()))
                raise SystemExit(error_message)

    @staticmethod
    def check_path_existence_only(check_path):
        """The method supports to find out existing gotten pathes
        If one of the gotten pathes is not exist, program is interupted
        """

        if os.path.exists(check_path):
            return 'full'
        else:
            dir_path, case_name = os.path.split(check_path)
            if os.path.exists(dir_path):
                return 'dir'
            else:
                error_message = f''' 
                    ------------------------------------------
                    The given name is not exist and directory {dir_path}
                    of the folder {case_name} is not exist as well.  
                    Above information can help you find where is it.
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


def copyFiele(root_src_dir, root_dst_dir, nameFilesOld='', nameFileNew=''):
    src_file = os.path.join(root_src_dir, nameFilesOld)
    dst_file = os.path.join(root_dst_dir, nameFileNew)
    shutil.copy2(src_file, dst_file)