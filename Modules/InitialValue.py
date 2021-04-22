import os
import sys

from Modules.AddtionalFunctions import changeVariablesFunV2
from distutils.dir_util import copy_tree


class IntiailValue():


    def __init__(self, pathCase=None, dictionary=None):
        self.pathCase = pathCase
        if pathCase == None:
            self.path = None
        else:
            self.path = os.path.join(pathCase, '0')
        self.dictionary = dictionary



    def setVarAllFiels(self, *varDict, pathCase=None):

        dictionary = self.priorityDictionary(varDict)
        path = self.priorityPath(pathCase)
        fileList = os.listdir(self.path)
        os.chdir(path)
        for file in fileList:
            for list in dictionary:
                for var in list:
                    changeVariablesFunV2(var, list[var], nameFile=file)


    def setVar(self, *varDict, nameFiels=['U', 'k'], pathCase=None):

        dictionary = self.priorityDictionary(varDict)
        path = self.priorityPath(pathCase)

        os.chdir(path)
        for file in nameFiels:
            for list in dictionary:
                for var in list:
                    changeVariablesFunV2(var, list[var], nameFile=file)



    def setMappSet(self, sourcePath=None, distPath=None, source='0', dist='0.25'):
        self.mappSettings = {}
        self.mappSettings['sPath'] = sourcePath
        self.mappSettings['dPath'] = distPath
        self.mappSettings['source'] = source
        self.mappSettings['dist'] = dist


    def mappValues(self, sourcePath=None, distPath=None, source=None, dist=None):



        sourcePath = os.path.join(pathSource, '0')
        distPath = os.path.join(pathNewCase, '0.25')
        copy_tree(sourcePath, distPath)

    def calcInitVal(self, A, B, Uin, nu):
        """The function serves to calculate intial values required for improving convergence of task. The function
        gives dictionaries with key of variables and them values. Keys of variables is chosen as way as in fiels of OF.
        Input variables:
        Uin is the inlet velocity
        nu is the kinematic viscosity
        Output variables
        Dh is hydrolic diametr
        Re is the Reynolds number
        I is the intensivity of flow
        L is mixing length scale
        k is predict kinetic energy
        omega is predict specific dissipation rate
        e is predict disspation rate"""
        Dh = 4 * A * B / (2 * (A + B))  # hydrolic diametr
        Re = Uin * Dh / nu  # Reynolds number
        I = 0.16 * Re ** (-0.125)  # Intensity
        L = Dh * I  # mix length    scale
        k = 1.5 * (I * Uin) ** 2  # kinetic energy
        omega = k ** 0.5 / (0.09 ** 0.25 * L)  # specific dissipation rate
        e = 0.09 ** 0.75 * k ** 1.5 / L  # dissipation rate
        dict = {'Dh_var': Dh,
                'Re_var': Re,
                'Ical_var': I,
                'L_var': L,
                'k_var': k,
                'omega_var': omega,
                'ep_var': e,
                }
        return dict


    def priorityDictionary(self, varDict):
        if varDict==None:
            if self.dictionary != None:
                return self.dictionary
            else:
                sys.exit('ERROR: The dictonary is not exist')
        else:
            return varDict

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
            return os.path.join(pathCase, '0')
