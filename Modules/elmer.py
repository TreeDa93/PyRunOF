import os
import pathlib as pl
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict, Any


class Elmer:
    """
    The clss is designed to provide manipulations on elmer settings in .sif file
    Attributes:
        ---------------
        path_case is the path of case where sif file is put
        sif_name is the name of sif file put in path_case and containing settings of elmer case
    """

    def __init__(self, path_case=None, sif_name=None):
        self.path_case = path_case
        self.sif_name = sif_name

    def set_elmer_var(self, *elmer_dicts: dict, path_case: str = None, sif_name: str = None):
        """
        The method to set given parameters in the file with sif extension.
        The general idea of the method is to find given part of text in sif file and to change
        the part of text on given value. You have to set the flags, keys of elmer_dicts,
        in the sif file yourselves for purpose of the method can find them and change it.
        It should be noted the flag to be unique.
        Input:
            elmer_dicts is a set of dictionaries with keys as names or flags of variable in sif file
            and values of the dictionaries as value to be set instead of the flags.
            paths_case is path of case where you need to provide tuning of sif file
            sif_name is the name of sif file put in path_case and containing settings of elmer case
        Output:

        """
        path_case = Priority.path(path_case, None, self.path_case)
        sif_name = Priority.name(sif_name, None, self.sif_name)
        if '.sif' not in sif_name:
            sif_name += '.sif'

        for elmer_dict in elmer_dicts:
            for var in elmer_dict:
                Files.change_var_fun(var, elmer_dict[var], path=path_case, file_name=sif_name)

    def set_elmer_case(self, sif_name: str = None, path_case: str = None):
        sif_name = Priority.name(sif_name, None, self.sif_name)

        path_case = Priority.path(path_case, None, self.path_case)

        if '.sif' not in sif_name:
            sif_name += '.sif'

    def set_elmer_path(self, sif_name: str = None, path_case: str = None):
        sif_name = Priority.name(sif_name, None, self.sif_name)

        path_case = Priority.path(path_case, None, self.path_case)

        if '.sif' not in sif_name:
            sif_name += '.sif'


class Elmer_new:
    """
    The clss is designed to provide manipulations on elmer settings in .sif file
    Attributes:
        ---------------
        path_case is the path of case where sif file is put
        sif_name is the name of sif file put in path_case and containing settings of elmer case
    """

    def __init__(self, key: Optional[str] = 'general',
                 case_path: Optional[str] = None,
                 sif_name: Optional[str] = None):
        self.info = dict.fromkeys([key], dict(path=pl.Path(case_path),
                                              name=sif_name))
        self.general_key = key

    def set_var(self, *elmer_dicts: dict,
                path_case: Optional[str] = None,
                sif_name: Optional[str] = None,
                info_key: Optional[str] = None):
        """
        The method to set given parameters in the file with sif extension.
        The general idea of the method is to find given part of text in sif file and to change
        the part of text on given value. You have to set the flags, keys of elmer_dicts,
        in the sif file yourselves for purpose of the method can find them and change it.
        It should be noted the flag to be unique.
        Input:
            elmer_dicts is a set of dictionaries with keys as names or flags of variable in sif file
            and values of the dictionaries as value to be set instead of the flags.
            paths_case is path of case where you need to provide tuning of sif file
            sif_name is the name of sif file put in path_case and containing settings of elmer case
        Output:

        """
        info_key = self._check_key(info_key)
        path_case = Priority.path_dict(path_case, 'path', self.info[info_key])
        sif_name = Priority.name(sif_name, 'name', self.info[info_key])
        sif_name = self._check_prefix_sif(sif_name)

        for elmer_dict in elmer_dicts:
            for var in elmer_dict:
                Files.change_var_fun(var, elmer_dict[var], path=path_case, file_name=sif_name)

    def set_case(self, sif_name: str = 'magnetic.sif',
                 info_key: Optional[str] = None) -> None:
        info_key = self._check_key(info_key)
        self.info[info_key]['name'] = sif_name

    def get_case(self, info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        return self.info[info_key]

    def set_path(self, path_case: Optional[str] = os.getcwd(),
                 info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        self.info[info_key] = dict(path=pl.Path(path_case),
                                              name=sif_name)

    def get_path(self, info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        return self.info[info_key]['path']

    def set_new_parameter(self, parameter: Any,
                          info_key: Optional[str] = None,
                          parameter_name: Optional[str] = 'new_parameter'):
        info_key = self._check_key(info_key)
        self.info[info_key][parameter_name] = parameter

    def get_any_parameter(self, parameter_name: Optional[str] = 'new_parameter',
                          info_key: Optional[str] = None,
                          ):
        info_key = self._check_key(info_key)
        return self.info[info_key][parameter_name]

    def find_all_sif(self, path_case: Optional[str] = None,
                info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        path_case = pl.Path(Priority.path_dict(path_case, 'path', self.info[info_key]))

        return list(path_case.glob('**/*.sif'))

    def _check_key(self, key):
        """
        Проверка задания ключа. Если ключ не задан берется ключ
        из аттрибута класса
        """
        if key is None:
            return self.general_key
        else:
            return key

    def _check_prefix_sif(self, sif_name):
        if '.sif' not in sif_name:
            sif_name += '.sif'
        return sif_name


