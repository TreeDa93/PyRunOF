import os, sys
from Modules.AddtionalFunctions import changeVariablesFunV2, copyFiele

class SetConstantParam():

    def __init__(self, pathCase=None, pathLib=''):
        self.pathCase = pathCase
        if pathCase == None:
            self.path = None
        else:
            self.path = os.path.join(pathCase, 'constant')

        self.pathLib = pathLib
        self.addPath = os.path.join(pathLib, 'AdditinalFiles', 'TurbulenceFiles')

    def setTransportProp(self, *lists):
        """The function sets given variables to transportProperties file
        patheNewCase is the path where transportProperties will be modificated
        lists are a number of dictionaries with keys, which called as name of variables to transportProperties,
        and values"""
        os.chdir(self.path)
        for spisok_var in lists:
            for var in spisok_var:
                changeVariablesFunV2(var, spisok_var[var], nameFile='transportProperties')

    def setTurbModel(self,typeTurbModel='kEpsilon', pathCase=None):
        """"The fucntion serves to set required turbulent model for solving task. For this purpose, one of list
          of wrriten files with given settings will be renamed into turbulenceProperties to system folder of adjusted case
        acording required type of rubulence model
        path_new_case is the path of the new case
        typeTurbModel is variables definding type of turbulence model
                LES
                kEpsilon
                realizableKE
                kOmega
                kOmegaSST
                """
        path = self.priorityPath(pathCase)
        os.chdir(path)

        if typeTurbModel == 'LES':
            os.rename('turbulenceProperties_LES', 'turbulenceProperties')
        elif typeTurbModel == 'kEpsilon':
            os.rename('turbulenceProperties_kEpsilon', 'turbulenceProperties')
        elif typeTurbModel == 'realizableKE':
            os.rename('turbulenceProperties_realizableK', 'turbulenceProperties')
        elif typeTurbModel == 'kOmega':
            os.rename('turbulenceProperties_kOmega', 'turbulenceProperties')
        elif typeTurbModel == 'kOmegaSST':
            os.rename('turbulenceProperties_kOmegaSST', 'turbulenceProperties')


    def setTurbModel2(self,typeTurbModel='kEpsilon', pathCase=None):
        """"The fucntion serves to set required turbulent model for solving task. For this purpose, one of list
          of wrriten files with given settings will be renamed into turbulenceProperties to system folder of adjusted case
        acording required type of rubulence model
        path_new_case is the path of the new case
        typeTurbModel is variables definding type of turbulence model
                LES
                kEpsilon
                realizableKE
                kOmega
                kOmegaSST
                """
        path = self.priorityPath(pathCase)
        if typeTurbModel == 'LES':
            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_LES', nameFileNew='turbulenceProperties')
        elif typeTurbModel == 'kEpsilon':
            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_kEpsilon',
                      nameFileNew='turbulenceProperties')
        elif typeTurbModel == 'realizableKE':

            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_realizableKE',
                      nameFileNew='turbulenceProperties')
        elif typeTurbModel == 'kOmega':

            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_kOmega',
                      nameFileNew='turbulenceProperties')
        elif typeTurbModel == 'kOmegaSST':
            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_kOmegaSST',
                      nameFileNew='turbulenceProperties')

        elif typeTurbModel == 'laminar':
            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_Laminar',
                      nameFileNew='turbulenceProperties')
        elif typeTurbModel == 'LESSmag':
            copyFiele(self.addPath, path, nameFilesOld='turbulenceProperties_LESdynamicSmag',
                      nameFileNew='turbulenceProperties')

    def setAnyConstantFiles(self, *listsVar, files=['controlDict'], pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""

        path = self.priorityPath(pathCase)
        os.chdir(path)
        for file in files:
            for spisok_var in listsVar:
                for var in spisok_var:
                    changeVariablesFunV2(var, spisok_var[var], nameFile=file)

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
            return os.path.join(pathCase, 'constant')