import os
import sys


class ParametricSweep:
    """
        #FIXIT

    """

    def __init__(self, *dicts, values={'keys': []}, fun=None):
        self.dictionaries = dicts
        self.values = values
        self.fun = fun
        self.currentIter = 0

    def run(self, generator_names=False):
        general_path = os.getcwd()
        while self.currentIter < self.numberCases:

            if generator_names is True:
                name = self._generator_name()
                self._change_vars()
                self.fun(name)
                os.chdir(general_path)
            else:
                self._change_vars()
                self.fun()
                os.chdir(general_path)

    def set_fun(self, fun1=None):
        """The method sets python function to be runned"""
        self.fun1 = fun1

    def set_sweep_dict(self, sweep_dict={'keys': [1, 2, 3]}):
        """The method sets dictionarie to be varied
        Проверяет правильно ли задано количество случаев,
        задает их количество и устанавливает словарь перебора
        """
        self.numberCases  = self._check_sweep_dict(sweep_dict)
        self.sweepDict = sweep_dict

    def set_find_dicts(self, find_dicts=[]):
        """The method sets dictionaries where it will be fiended varieng variables"""
        self.find_dicts = find_dicts

    def _change_vars(self):
        """The methos change values of variables in dictionaries"""
        for dic in self.find_dicts:
            for key in self.sweepDict:
                if key in dic:
                    dic[key] = self.sweepDict[key][self.currentIter]
        print(self.find_dicts[:])
        self.currentIter+=1

    @staticmethod
    def _check_sweep_dict(sweep_dict):
        #FIXME it can be static
        i = 0
        for key in sweep_dict:
            if i == 0:
                print(len(sweep_dict[key]))
                tester = len(sweep_dict[key])
            else:
                if tester != len(sweep_dict[key]):
                    sys.exit('The sweep array numbers have different size')
                else:
                    tester = len(sweep_dict[key])
            i+=1
        return tester

    def _generator_name(self):
        name = str()
        for dic in self.find_dicts:
            for key in self.sweepDict:
                if key in dic:
                    name += str(f'{key}_{self.sweepDict[key][self.currentIter]}')
        return name



