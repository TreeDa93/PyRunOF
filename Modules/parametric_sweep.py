import os
import sys
import pathlib as pl


import Modules.manipulations
from Modules.auxiliary_functions import Priority, Files, Executer
from Modules.manipulations import Manipulations
from Modules.information import Information

class ParametricSweep(Information):
    """
        #FIXIT

    """
    def __init__(self, *dicts, values={'keys': []}, fun=None, info_key='general'):
        self.currentIter = 0
        self.info = dict.fromkeys([info_key], dict(fun=fun))
        
        

    def run(self, parameters_path, sweep_params={}):
        while self.currentIter < self.numberCases:
            cur_dict = dict()
            for key in sweep_params:
                cur_dict[key] = sweep_params[key][self.currentIter]

            path = pl.Path(parameters_path)
            save_path = path.parent / (path.stem + f' {self.currentIter}')
            Manipulations.change_json_params(parameters_path=parameters_path,
                                             save_path=save_path,
                                             changed_parameters=sweep_params)
            new_params = Files.open_json(save_path)
            
    def run_new(self, fun=None):

        while self.currentIter < 0:
            Priority.variable(fun, where=self.info, var_key='fun')()
        
        
    
    def built_parameters(self):
        Files.open_json(file_path=)
        
            
        
        
    def run_old(self, generator_names=False):
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
        
    def 

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



