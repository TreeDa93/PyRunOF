import sys, os
from Modules.AddtionalFunctions import changeVariablesFunV2

class Elmer():


    def __init__(self, pathCase=None, sifName='.sif'):
        self.pathCase = pathCase
        self.sifName = sifName

    def setElmerVar(self, *elmerDictioaries, pathCase=None, sifName=None):

        path = self.priorityPath(pathCase)
        sifName = self.prioritysifFile(sifName)
        os.chdir(path)
        for list in elmerDictioaries:
            for var in list:
                changeVariablesFunV2(var, list[var], nameFile=sifName)




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
                return self.pathCase
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return pathCase

    def prioritysifFile(self, sifName):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if sifName == None:
            if self.sifName != None:
                return self.sifName
            else:
                sys.exit('Error: You do not enter the name of the sif file!!!')
        else:
            return sifName





