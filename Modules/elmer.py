import sys
import os
from Modules.auxiliary_functions import change_var_fun
from Modules.auxiliary_functions import Priority


class Elmer(Priority):
    """
    FIXME
    """

    def __init__(self, path_case=None, sif_name='.sif'):
        self.path_case = path_case
        self.sif_name = sif_name

    def set_elmer_var(self, *elmerDictioaries, path_case=None, sif_name=None):
        """
        FIXME need add description
        :param elmerDictioaries:
        :param path_case:
        :param sif_name:
        :return:
        """
        path = self._priority_path(path_case)
        sif_name = self._priority_sif_file(sif_name)
        os.chdir(path)
        for var_list in elmerDictioaries:
            for var in var_list:
                change_var_fun(var, var_list[var], nameFile=sif_name)

    def _priority_path(self, path_case):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if path_case is None:
            if self.path_case is not None:
                return self.path_case
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return path_case

    def _priority_sif_file(self, sif_name):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if sif_name is None:
            if self.sif_name is None:
                return self.sif_name
            else:
                sys.exit('Error: You do not enter the name of the sif file!!!')
        else:
            return sif_name






