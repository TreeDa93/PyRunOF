import os
import sys
import pathlib as pl
import itertools as it
from functools import wraps
from typing import Sequence
from tqdm import tqdm

from .manipulations import Manipulations
from ..additional_fun.auxiliary_functions import Priority
from ..additional_fun.information import Information


class ParametricSweep(Information):
    """
    FIXME
    """

    def __init__(self, fun=None):

        self.cur_i: int = 1
        self.run_fun = fun


    def run(self, ps_params, fun=None, update_vars=None, type_set='special series'):
        """


        Args:
            ps_params [dict]: parameters of the
            fun [callable]:
            update_vars [list of dicts]: list of updated variables
            type_set [string]: type of generation cases of variables

        Returns: None

        """
        self._prepare_ps_dict(ps_params, type_set=type_set)
        for self.cur_data in self.set:
            if update_vars is not None:
                self._update_variables(update_vars)
            run_fun = Priority.variable(fun, where=self.run_fun)
            run_fun(self)
            self.cur_i += 1

    def run_progress_bar(self, ps_params, fun=None, update_vars=None, type_set='special series'):
        """


        Args:
            ps_params [dict]: parameters of the
            fun [callable]:
            update_vars [list of dicts]: list of updated variables
            type_set [string]: type of generation cases of variables

        Returns: None

        """
        self._prepare_ps_dict(ps_params, type_set=type_set)

        for self.cur_data in tqdm(self.set, total=self.n_iter, initial=1):
            tqdm.write('Current parameters in parametric sweep:')
            for name_var, val in self.cur_data.items():
                tqdm.write(f'{name_var}: \t {val}')
            if update_vars is not None:
                self._update_variables(update_vars)
            run_fun = Priority.variable(fun, where=self.run_fun)
            run_fun(self)
            self.cur_i += 1

    def get_cur_name(self, type_name='index'):

        if type_name == 'index':
            return str(self.cur_i)
        else:
            name = str()
            for key, val in self.set[self.cur_i].items():
                name += str(f'_{key}_{val}')
            return name

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
            self.n_iter = len(list(it.product(*ps_set))) + 1
        elif type_set == 'special series':
            iterator = zip(*ps_set)
            self.n_iter = len(list(zip(*ps_set))) + 1
        elif type_set == 'series':
            self._check_sweep_dict(ps_dict)
            iterator = zip(*ps_set)
            self.n_iter = len(list(zip(*ps_set))) + 1
        else:
            print('WARNING!!! Yuo write no correct type of set, because the procedure was done as all combination')
            iterator = it.product(*ps_set)

        self.set = [self._merge_dicts(entry) for entry in iterator]
        self.type_set = type_set

        

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

    def _update_variables(self, update_vars):
        assert type(update_vars) is tuple, 'The argument update_vars should be tuple!'
        for data_dict in update_vars:
            assert type(data_dict) is dict, 'Each element of update_vars should be dictionary!!!'
            data_dict.update(self.cur_data)
