import os
from Modules.AddtionalFunctions import changeVariablesFunV2
from distutils.dir_util import copy_tree
class IntiailValue():


    def __init__(self, pathNewCase=''):
        self.pathNewCase = pathNewCase
        self.path = os.path.join(pathNewCase, '0')


    def setVariablesValue(self, *varDict):
        if varDict==None:
            dictionary = self.dictionary
        else:
            dictionary = varDict

        fileList = os.listdir(self.path)
        os.chdir(self.path)
        for file in fileList:
            for list in dictionary:
                for var in list:
                    print(var)
                    changeVariablesFunV2(var, list[var], nameFile=file)


    def mappValues(self, sourcePath, distPath):
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

