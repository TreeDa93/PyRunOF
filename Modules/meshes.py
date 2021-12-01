import os
import sys
from Modules.auxiliary_functions import change_var_fun
from Modules.auxiliary_functions import Priority

class Mesh:
    """
    FIXME

    """

    def __init__(self, case_path=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.case_path = case_path
        if case_path == None:
            self.path = None
        else:
            self.path = os.path.join(case_path, 'system')

    def set_blockMesh(self, mesh_list, case_path=None):
        """The fucntion sets given variables to blockMeshDict file
        meshList is the dictionary with variables and name of the variables, which will be set at blockMeshDict file
        """
        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        os.chdir(case_path)
        for keys in mesh_list:
            change_var_fun(keys, mesh_list[keys], nameFile='blockMeshDict')

        print('The file blockMesh is set!')

    def run_blockMesh(self, case_path=None):
        """The function creates mesh by blockMesh OpenFOAM utilite"""

        case_path = self.priorityPath2(case_path)
        os.chdir(case_path)
        os.system('blockMesh')


    def run_gMesh_to_Elmer(self, case_path=None):
        case_path = self.priorityPath2(case_path)
        os.chdir(case_path)
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
            if self.case_path != None:
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
            if self.case_path != None:
                return self.case_path
            else:
                sys.exit('Error: You do not enter the base name!!!')
        else:
            return pathCase
