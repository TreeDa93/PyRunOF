import os
import pathlib as pl
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict, Any


class Information:
    """
    elmer_info = {'general':{path: 'etc/home ...', name: 'magnetic.sif'
                'additional1':{path: 'etc/home/new1 ...', name2: 'magnetic2.sif'
                'general':{path: 'etc/home/new3 ...', name3: 'magnetic3.sif'
                }
    """

    def __init__(self, info_key: Optional[str] = 'general',
                 case_path: Optional[str] = None,
                 sif_name: Optional[str] = None):

        self.info = dict.fromkeys([info_key], dict(path=pl.Path(case_path),
                                                   name=sif_name))

    def set_case(self, sif_name: str = 'magnetic.sif',
                 info_key: Optional[str] = None) -> None:
        info_key = self.get_key(info_key)
        self.info[info_key]['name'] = sif_name

    def set_path(self, path_case: Optional[str] = pl.Path.cwd(),
                 info_key: Optional[str] = None):
        info_key = self.get_key(info_key)
        self.info[info_key]['path'] = path_case

    def get_case(self, info_key: Optional[str] = None):
        info_key = self.get_key(info_key)
        return self.info[info_key]['name']

    def get_path(self, info_key: Optional[str] = None):
        info_key = self.get_key(info_key)
        return self.info[info_key]['path']

    def get_general_key(self):
        return list(self.info.keys())[0]

    def get_key(self, key):
        """
        Проверка задания ключа. Если ключ не задан берется ключ
        из аттрибута класса
        """
        if key is None:
            return self.get_general_key()
        else:
            return key

    def set_new_parameter(self, parameter: Any,
                          info_key: Optional[str] = None,
                          parameter_name: Optional[str] = 'new_parameter'):
        info_key = self.get_key(info_key)
        self.info[info_key][parameter_name] = parameter

    def get_any_parameter(self, parameter_name: Optional[str] = 'new_parameter',
                          info_key: Optional[str] = None,
                          ):
        info_key = self.get_key(info_key)
        return self.info[info_key][parameter_name]

    def find_all_sif(self, path_case: Optional[str] = None,
                     info_key: Optional[str] = None):
        info_key = self.get_key(info_key)
        path_case = Priority.path(path_case, self.info[info_key], path_key='path')

        return list(path_case.glob('**/*.sif'))

    def find_all_zero_files(self, path_case: Optional[str] = None,
                     info_key: Optional[str] = None):
        """
        The method is srved to find all files in zero folder of OpenFoam case,
        for example U, p etc.
        Input:
            path_case is the path of openfoam case
            info_key is the
        """
        info_key = self.get_key(info_key)
        path_case = Priority.path(path_case, self.info[info_key], path_key='path')
        zero_folder_path = path_case / '0'
        return list(zero_folder_path.glob('**/*.sif'))

    def __init_elmer__(self, info_key: Optional[str] = 'general',
                       case_path: Optional[str] = None,
                       sif_name: Optional[str] = None):
        self.info = dict.fromkeys([info_key], dict(path=self._check_type_path(case_path),
                                                   name=sif_name))

    def __init_constant__(self, info_key: Optional[str] = 'general',
                          case_path: Optional[str] = None,
                          lib_path: Optional[str] = None):
        self.info = dict.fromkeys([info_key], dict(path=self._check_type_path(case_path),
                                                   lib_path=self._check_type_path(lib_path)))

    def __init_iv__(self, info_key: Optional[str] = 'general',
                    case_path: Optional[str] = None):
        self.info = dict.fromkeys([info_key],
                                  dict(path=self._check_type_path(case_path)))


    def __init_mesh__(self, info_key: Optional[str] = 'general',
                       case_path: Optional[str] = None,
                       elmer_mesh_name: Optional[str] = None):
        # FIXME
        self.info = dict.fromkeys([info_key], dict(path=self._check_type_path(case_path),
                                                   elmer_mesh_name=elmer_mesh_name))


    @staticmethod
    def _check_type_path(path):
        if type(path) in [str, os.PathLike, pl.PosixPath, pl.WindowsPath]:
            return pl.Path(path)
        else:
            return None

    @staticmethod
    def _check_prefix_sif(sif_name):
        if '.sif' not in sif_name:
            sif_name += '.sif'
        return sif_name

