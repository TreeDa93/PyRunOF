import os
import sys
import pathlib as pl
import itertools as it

from Modules.auxiliary_functions import Priority, Files, Executer
from Modules.manipulations import Manipulations
from Modules.information import Information

class ParametricSweep(Information):
    """
    FIXME
    """

    def __init__(self, fun=None, info_key='general'):
        self.info = dict.fromkeys([info_key], dict(fun=fun,
                                                   json_path=None))
        self.cur_i: int = 0
        self.last_i = 0

    def run_new(self, path_json, ps_params, fun=None, type_new=True, info_key=None):
        self.last_i = self._check_sweep_dict(ps_params)
        info_key = self.get_key(info_key)
        while self.cur_i < self.last_i:
            self._parameters_by_json(path_json, ps_params, type_new=type_new)
            Priority.variable(fun, where=self.info[info_key], var_key='fun')(self.info[info_key]['json_path_current'])
            self.cur_i += 1




    def run_old(self, generator_names=False):
        general_path = os.getcwd()
        while self.cur_i < self.numberCases:

            if generator_names is True:
                name = self._generator_name()
                self._change_vars()
                self.fun(name)
                os.chdir(general_path)
            else:
                self._change_vars()
                self.fun()
                os.chdir(general_path)

    def set_fun(self, fun1=None, info_key='general'):
        """The method sets python function to be runned"""
        self.info[info_key] = fun1

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
                    dic[key] = self.sweepDict[key][self.cur_i]
        print(self.find_dicts[:])
        self.cur_i+=1



    def _parameters_by_json(self, path_json, ps_params:dict,
                            type_new=True, info_key=None):
        """
        """
        if type_new is True:
            path_json_new = pl.Path(path_json).parent / (pl.Path(path_json).stem + '_case_' + str(self.cur_i)+'.json')
        else:
            path_json_new = path_json

        cur_params = dict()

        for key, value in ps_params.items():
            cur_params[key] = value[self.cur_i]

        info_key = self.get_key(info_key)
        self.info[info_key]['json_path_current'] = path_json_new
        Manipulations.change_json_params(path_json, cur_params, save_path=path_json_new)



    @staticmethod
    def _check_sweep_dict(sweep_dict):
        #FIXME it can be static
        i = 0
        for key in sweep_dict:
            if i == 0:
                tester = len(sweep_dict[key])
            else:
                if tester != len(sweep_dict[key]):
                    sys.exit('The sweep array numbers have different size')
                else:
                    tester = len(sweep_dict[key])
            i+=1
        return tester

    @staticmethod
    def _chech_numbers_cases(sweep_dict):
        pass


    def _generator_name(self):
        name = str()
        for dic in self.find_dicts:
            for key in self.sweepDict:
                if key in dic:
                    name += str(f'{key}_{self.sweepDict[key][self.currentIter]}')
        return name



