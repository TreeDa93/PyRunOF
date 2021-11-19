import os
import sys
from Modules.auxiliary_functions import change_var_fun


class Mesh:
    """
    FIXME

    """

    def __init__(self, pathCase=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.pathCase = pathCase
        if pathCase == None:
            self.path = None
        else:
            self.path = os.path.join(pathCase, 'system')



    def setBlockMesh(self, meshList, pathCase=None):
        """The fucntion sets given variables to blockMeshDict file
        meshList is the dictionary with variables and name of the variables, which will be set at blockMeshDict file
        """
        pathCase = self.priorityPath(pathCase)
        os.chdir(pathCase)
        for keys in meshList:
            change_var_fun(keys, meshList[keys], nameFile='blockMeshDict')

        print('The file blockMesh is set!')

    def runBlockMesh(self, pathCase=None):
        """The function creates mesh by blockMesh OpenFOAM utilite"""

        pathCase = self.priorityPath2(pathCase)
        os.chdir(pathCase)
        os.system('blockMesh')


    def runElmerMesh(self, pathCase=None):
        pathCase = self.priorityPath2(pathCase)
        os.chdir(pathCase)
        os.system(f'gmsh -3 {self.elmerMeshName}.geo')
        os.system(f'ElmerGrid 14 2 {self.elmerMeshName} -autoclean ')



    def settingsElmerMesh(self, meshList, pathCase=None, elmerMeshName=''):
        pathCase = self.priorityPath2(pathCase)
        os.chdir(pathCase)
        print(os.getcwd())
        self.elmerMeshName = elmerMeshName
        for keys in meshList:
            change_var_fun(keys, meshList[keys], nameFile=f'{self.elmerMeshName}.geo')

    def priorityPath(self, pathCase):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if pathCase == None:
            if self.pathCase != None:
                return self.path
            else:
                sys.exit('Error: You do not enter the base name!!!')
        else:
            return os.path.join(pathCase, 'system')

    def priorityPath2(self, pathCase):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if pathCase == None:
            if self.pathCase != None:
                return self.pathCase
            else:
                sys.exit('Error: You do not enter the base name!!!')
        else:
            return pathCase
