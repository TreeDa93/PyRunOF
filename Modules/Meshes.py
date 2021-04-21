import os

from Modules.AddtionalFunctions import changeVariablesFunV2

class Mesh():

    def __init__(self, pathNewCase=''):
        self.pathNewCase = pathNewCase
        self.path = os.path.join(pathNewCase, 'system')


    def setBlockMesh(self, meshList):
        """The fucntion sets given variables to blockMeshDict file
        meshList is the dictionary with variables and name of the variables, which will be set at blockMeshDict file
        """
        os.chdir(self.path)
        for keys in meshList:
            changeVariablesFunV2(keys, meshList[keys], nameFile='blockMeshDict')

        print('The file blockMesh is set!')

    def createOFMesh(self, pathNewCase):
        """The function creates mesh by blockMesh OpenFOAM utilite"""
        os.chdir(pathNewCase)
        os.system('blockMesh')



    def setElmerMesh(self):
        pass