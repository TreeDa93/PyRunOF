import os
from AddtionalFunctions import changeVariablesFunV2

class SetConstantParam():

    def setTransportProp(self, pathNewCase, *lists):
        """The function sets given variables to transportProperties file
        patheNewCase is the path where transportProperties will be modificated
        lists are a number of dictionaries with keys, which called as name of variables to transportProperties,
        and values"""
        os.chdir(os.path.join(pathNewCase, 'constant'))
        for spisok_var in lists:
            for var in spisok_var:
                changeVariablesFunV2(var, spisok_var[var], nameFile='transportProperties')

    def setTurbModel(self, pathNewCase, typeTurbModel='kEpsilon'):
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
        os.chdir(os.path.join(pathNewCase, 'constant'))
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