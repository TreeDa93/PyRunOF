import os
import sys
import shutil


def change_var_fun(dist_var, sour_var, nameFile=''):
    """Function to find and replace required text part at given file
            dist_var is the depicts finding variables
            sour_var depicts replacing variables
            nameFile is the name of file where the procedure will be done

    """
    if os.path.isfile(nameFile):
        with open(nameFile, 'r') as f:
            oldData = f.read()
        newData = oldData.replace(str(dist_var), str(sour_var))
        with open(nameFile, 'w') as f:
            f.write(newData)
    else:
        print(f'Warning: The file {nameFile} is not exist!')


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


class AddtionalFun:
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

    def change_text(self, dist_var, sour_var, name_file=''):
        """Function to find and replace required text part at given file
        dist_var is the depicts finding variables
        sour_var depicts replacing variables
        nameFile is the name of file where the procedure will be done

        """

        if os.path.isfile(dist_var):
            with open(sour_var, 'r') as f:
                oldData = f.read()
            newData = oldData.replace(str(dist_var), str(sour_var))
            with open(name_file, 'w') as f:
                f.write(newData)
        else:
            print(f'Warning: The file {name_file} is not exist!')


class Priority:

    def __init__(self, names_cases=None, paths=None, sif_name='.sif', file=None):
        self.paths = paths
        self.names_cases = names_cases
        self.sifName = sif_name
        self.file = file

    def priority_path(self, path_case, path_key=''):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if path_case is None:
            if self.paths[path_key] is not None:
                return self.paths[path_key]
            else:
                #sys.exit('Error: You do not enter the name of the sif file!!!')
                raise SystemExit(f'Error: You do not set {path_key} path!!!')
        else:
            return path_case

    def priority_path(self, path_case, path_key=''):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if path_case is None:
            if self.paths[path_key] is not None:
                return self.paths[path_key]
            else:
                #sys.exit('Error: You do not enter the name of the sif file!!!')
                raise SystemExit(f'Error: You do not set {path_key} path!!!')
        else:
            return path_case

    def check_path_key(self, key):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if key in self.paths.keys():
            pass
        else:
            raise SystemExit(f'You write wrong key!!!')

    def check_key(self, key, where):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if key in where:
            pass
        else:
            raise SystemExit(f'You write wrong key!!!')

    def priority_name(self, case_name, name_key=''):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrun BasePath, returnNewPath is selected pathes acording priority
        """
        if case_name is None:
            if self.paths is not None:
                return self.names_cases[name_key]
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return case_name

    def file(self, file):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
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
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
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

    def _priority_cores(self, core_OF):
        if core_OF is None:
            if self.core_OF is not None:
                return self.core_OF
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
