import pathlib as pl
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict, Any


class ElmerInfo:
    """
    elmer_info = {'general':{path: 'etc/home ...', name: 'magnetic.sif'
                'additional1':{path: 'etc/home/new1 ...', name2: 'magnetic2.sif'
                'general':{path: 'etc/home/new3 ...', name3: 'magnetic3.sif'
                }
    """

    def __init__(self, info_key: Optional[str] = 'general',
                 case_path: Optional[str] = None,
                 sif_name: Optional[str] = None):

        self.elmer_info = dict.fromkeys([info_key], dict(path=pl.Path(case_path),
                                                         name=sif_name))
        self.general_key = info_key

    def set_case(self, sif_name: str = 'magnetic.sif',
                 info_key: Optional[str] = None) -> None:
        info_key = self._check_key(info_key)
        self.elmer_info[info_key]['name'] = sif_name

    def set_path(self, path_case: Optional[str] = pl.Path.cwd(),
                 info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        self.elmer_info[info_key]['path'] = path_case

    def get_case(self, info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        return self.elmer_info[info_key]['name']

    def get_path(self, info_key: Optional[str] = None):
        info_key = self._check_key(info_key)
        return self.elmer_info[info_key]['path']

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
        path_case = pl.Path(Priority.path_dict(path_case, 'path', self.elmer_info[info_key]))

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


class Information(ElmerInfo):

    def __init__(self, path='test', sif_name=None):
        ElmerInfo.__init__(self)
