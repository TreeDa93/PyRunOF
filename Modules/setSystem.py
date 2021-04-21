from Modules.AddtionalFunctions import changeVariablesFunV2
import os

class SetSystem():

    def __init__(self, pathNewCase):
        self.pathNewCase = pathNewCase
        self.path = os.path.join(pathNewCase, 'system')

    def setControlDict(self, *lists):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        os.chdir(self.path)
        for spisok_var in lists:
            for var in spisok_var:
                changeVariablesFunV2(var, spisok_var[var], nameFile='controlDict')


