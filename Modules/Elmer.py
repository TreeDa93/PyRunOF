import sys, os
from Modules.AddtionalFunctions import changeVariablesFunV2

class Elmer():


    def __init__(self, pathCase=None, nameFile='.sif'):
        self.pathCase = pathCase

    def setElmerVar(self, *elmerDictioaries, pathCase=None, nameFile='.sif'):

        path = self.priorityPath(pathCase)
        os.chdir(path)
        for list in elmerDictioaries:
            for var in list:
                changeVariablesFunV2(var, list[var], nameFile=nameFile)


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
            return pathCase





