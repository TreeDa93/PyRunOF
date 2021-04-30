import os
import sys

import numpy as np


class ParametricSweep():


    def __init__(self, *dicts, values={'keys': []}, fun=None):
        self.dictionaries = dicts
        self.values=values
        self.fun = fun
        self.currentIter = 0


    def setFun(self, fun1=None):
        self.fun1 = fun1



    def run(self):
        generalPath = os.getcwd()

        while self.currentIter < self.numberCases:

            name = self.generatorName()
            self.changeVariables()
            self.fun(name)
            os.chdir(generalPath)


    def getSweepDict(self, dict={'keys': [1, 2, 3]}):
            self.numberCases  = self.checkSweepDict(dict)
            self.sweepDict = dict



    def getDicts(self, dicts=[]):
        self.dicts = dicts



    def changeVariables(self):

        for dic in self.dicts:
            for key in self.sweepDict:
                if key in dic:
                    dic[key] = self.sweepDict[key][self.currentIter]
        print(self.dicts[:])
        self.currentIter+=1

    def checkSweepDict(self, dict):

        i = 0
        for key in dict:
            if i == 0:
                print(len(dict[key]))
                tester = len(dict[key])
            else:
                if tester != len(dict[key]):
                    sys.exit('The sweep array numbers have different size')
                else:
                    tester = len(dict[key])
            i+=1

        return tester

    def generatorName(self):
        name = str()
        for dic in self.dicts:
            for key in self.sweepDict:
                if key in dic:
                    name += str(f'{key}_{self.sweepDict[key][self.currentIter]}')
        return name



