import os
import sys
import pathlib as pl
import itertools as it
from functools import partial, wraps
from typing import Callable, Sequence
from io import IOBase

from Modules.auxiliary_functions import Priority, Files, Executer
from Modules.manipulations import Manipulations
from Modules.information import Information


class ParametricSweep(Information):
    """
    FIXME
    """

    def __init__(self, fun=None, info_key='general', ):

        self.info = dict.fromkeys([info_key], dict(fun=fun,
                                                   json_path=None))
        self.cur_i: int = 0
        self.run_fun = None
        self.json_paths = list()

    def run(self, path_json, ps_params, fun=None, type_new=True, info_key=None):
        info_key = self.get_key(info_key)
        self._prepare_ps_dict(ps_params, type_set='all')
        for cur_data in self.info['Set']:
            self._update_json(path_json, cur_data, type_new=type_new)
            run_fun = Priority.variable(fun, where=self.run_fun)
            run_fun(self)
            self.cur_i += 1

    def get_cur_name(self, type_name='index'):

        if type_name == 'index':
            return str(self.cur_i)
        else:
            name = str()
            for key, val in self.info['Set'][self.cur_i]:
                name += str(f'{key}_{val}')

    def get_cur_json_path(self):
        return self.json_paths[self.cur_i]


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
        self.numberCases = self._check_sweep_dict(sweep_dict)
        self.sweepDict = sweep_dict

    def set_find_dicts(self, find_dicts=[]):
        """The method sets dictionaries where it will be fiended varieng variables"""
        self.find_dicts = find_dicts

    def _prepare_ps_dict(self, ps_dict, type_set='all'):
        """
            The method prepares generator of parameters for all iterations of parametric study.
            The generator return
        Args:
            ps_dict: dictionary with changing parameters of variables.
            combination: how to do sweep. Type 'all' means to take all possible combination.
                                            Type 'series' means to take sweep in the order they are mentioned.

        Returns:

        """

        ps_set = [[{key: entry} for entry in ps_dict[key]] for key in ps_dict]
        if type_set == 'all':
            iterator = it.product(*ps_set)
        elif type_set == 'special series':
            iterator = zip(*ps_set)
        elif type_set == 'series':
            self._check_sweep_dict(ps_dict)
            iterator = zip(*ps_set)
        else:
            print('WARNING!!! Yuo write no correct type of set, because the procedure was done as all combination')
            iterator = it.product(*ps_set)
        self.info['Set'] = [self._merge_dicts(entry) for entry in iterator]
        self.info['Type of param set'] = type_set

    def _change_vars(self):
        """The methos change values of variables in dictionaries"""
        for dic in self.find_dicts:
            for key in self.sweepDict:
                if key in dic:
                    dic[key] = self.sweepDict[key][self.cur_i]
        print(self.find_dicts[:])
        self.cur_i += 1

    def _update_json(self, path_json:str, cur_params: dict, type_new=True):
        if type_new is True:
            path_json_new = pl.Path(path_json).parent / (pl.Path(path_json).stem + '_case_' + str(self.cur_i) + '.json')
        Manipulations.change_json_params(path_json, cur_params, save_path=path_json_new)
        self.json_paths.append(path_json_new)

    def _parameters_by_json(self, path_json, ps_params: dict,
                            type_new=True, info_key=None):
        """
        """
        if type_new is True:
            path_json_new = pl.Path(path_json).parent / (pl.Path(path_json).stem + '_case_' + str(self.cur_i) + '.json')
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
        # FIXME it can be static
        i = 0
        for key in sweep_dict:
            if i == 0:
                tester = len(sweep_dict[key])
            else:
                if tester != len(sweep_dict[key]):
                    sys.exit('The sweep array numbers have different size')
                else:
                    tester = len(sweep_dict[key])
            i += 1
        return tester

    @staticmethod
    def _merge_dicts(args: Sequence[dict]):
        dct = {}
        for entry in args:
            dct.update(entry)
        return dct

    def _generator_name(self):
        name = str()
        for dic in self.find_dicts:
            for key in self.sweepDict:
                if key in dic:
                    name += str(f'{key}_{self.sweepDict[key][self.currentIter]}')
        return name
