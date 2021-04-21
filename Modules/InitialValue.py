import os
from AddtionalFunctions import changeVariablesFunV2
from distutils.dir_util import copy_tree
class IntiailValue():


    def __init__(self, pathNewCase):
        self.pathNewCase = pathNewCase
        self.path = os.path.join(pathNewCase, '0')


    def setVariablesValue(self, *varDict):
        if varDict==None:
            dictionary = self.dictionary
        else:
            dictionary = varDict

        fileList = os.listdir(self.path)

        for file in fileList:
            for list in dictionary:
                for var in list:
                    changeVariablesFunV2(var, list[var], nameFile=file)

    def mappValues(self, sourcePath, distPath):
        sourcePath = os.path.join(pathSource, '0')
        distPath = os.path.join(pathNewCase, '0.25')
        copy_tree(sourcePath, distPath)


