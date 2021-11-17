import os
import sys
from Modules.AddtionalFunctions import change_var_fun


class SetSystem:
    """
    #FIXIT

    """

    def __init__(self, pathCase=None):
        """PathCase is path where the class will be doing any manipulation"""
        self.pathCase = pathCase
        if pathCase == None:
            self.path = None
        else:
            self.path = os.path.join(pathCase, 'system')

    def setControlDict(self, *listsControlDicts, pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = self.priorityPath(pathCase)
        os.chdir(path)
        for spisok_var in listsControlDicts:
            for var in spisok_var:
                change_var_fun(var, spisok_var[var], nameFile='controlDict')

    def setfvSolution(self, *listsfvSolution, pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = self.priorityPath(pathCase)
        os.chdir(path)
        for spisok_var in listsfvSolution:
            for var in spisok_var:
                change_var_fun(var, spisok_var[var], nameFile='fvSolution')

    def setfvSchemes(self, *listsfvSchemes, pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = self.priorityPath(pathCase)
        os.chdir(path)
        for spisok_var in listsfvSchemes:
            for var in spisok_var:
                change_var_fun(var, spisok_var[var], nameFile='fvSchemes')

    def setAnyFiles(self, *listsVar, files=['controlDict'], pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""

        path = self.priorityPath(pathCase)
        os.chdir(path)
        for file in files:
            for spisok_var in listsVar:
                for var in spisok_var:
                    change_var_fun(var, spisok_var[var], nameFile=file)



    def priorityPath(self, pathCase):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """

        if pathCase == None:
            if self.pathCase != None:
                return self.path
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return os.path.join(pathCase, 'system')



