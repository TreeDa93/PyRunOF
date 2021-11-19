import os
import sys
from Modules.auxiliary_functions import change_var_fun


class SetSystem:
    """
    #FIXIT

    """

    def __init__(self, path_case=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.path_case = path_case
        if path_case is None:
            self.path = None
        else:
            self.path = os.path.join(path_case, 'system')

    def set_control_dict(self, *lists_controlDicts, path_case=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        path = self._priorityPath(path_case)
        os.chdir(path)
        for list_var in lists_controlDicts:
            for var in list_var:
                change_var_fun(var, list_var[var], nameFile='controlDict')

    def set_fvSolution(self, *listsfvSolution, path_case=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        path = self._priorityPath(path_case)
        os.chdir(path)
        for list_var in listsfvSolution:
            for var in list_var:
                change_var_fun(var, list_var[var], nameFile='fvSolution')

    def set_fvSchemes(self, *listsfvSchemes, path_case=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        path = self._priorityPath(path_case)
        os.chdir(path)
        for list_var in listsfvSchemes:
            for var in list_var:
                change_var_fun(var, list_var[var], nameFile='fvSchemes')

    def set_any_files(self, *listsVar, files=['controlDict'], path_case=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""

        path = self._priorityPath(path_case)
        os.chdir(path)
        for file in files:
            for list_var in listsVar:
                for var in list_var:
                    change_var_fun(var, list_var[var], nameFile=file)

    def _priorityPath(self, path_case):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """

        if path_case is None:
            if self.path_case is not None:
                return self.path
            else:
                sys.exit('Error: You do not enter the base name!!!')
        else:
            return os.path.join(path_case, 'system')



