import os
import pathlib as pl
from typing import List, Optional, Any
from .auxiliary_functions import Priority


class Information:
    """
    elmer_info = {'general': {path: 'etc/home ...', 
                             'name': 'magnetic.sif'
                             ...
                             others
                             ...
                             }
                'additional1':{path: 'etc/home/new1 ...', 
                               name2: 'magnetic2.sif'
                               }
                'other_params':{path: 'etc/home/new3 ...', 
                                'name3': 'magnetic3.sif'}
                }
    """

    def __init__(self, info_key: Optional[str] = 'general',
                 case_path: Optional[str] = None):
        self.info = dict.fromkeys([info_key], dict(path=pl.Path(case_path)))


    def get_name(self, name_key: str, info_key=None) -> str:
        """The method returns the name according given key
        Arguments:

            * name_key [str]
            * info_key [str, optional]
        
        """
        return Priority.name(name_key, self.info[self.get_key(info_key)]['case_names'])


    def create_name(self, *case_names: List[str],
                    name_base: str = '',
                    name_key: Optional[str] = 'new',
                    splitter: Optional[str] = '_',
                    only_base: Optional[bool] = False,
                    info_key=None) -> None:
        """The function create case name as
            if only_base is False:
                new_name = name_base + splitter + case_names[0] ... + case_names[-1]
            else:
                new_name = name_base
            Arguments: 
                * case_names [collection of strings] is the set of string to assemble new name
                * name_base [string] is the string to express general name part 
                * name_key [hashable] is the key to get the string to express general name part from dictionary
                * splitter [string] is the special symbol to splite base and additional parts of assembling name
                * only_base [bool] is the flag to detect requrments to extend name by additional parts.
                * info_key [hashable] is the key to store finile name in information dict. 
                """

        if only_base is True:
            self.info[self.get_key(info_key)]['case_names'][name_key] = name_base
            return name_base
        else:
            for addName in case_names:
                name_base += splitter + str(addName)

            self.info[self.get_key(info_key)]['case_names'][name_key] = name_base


    def create_path_from_dir(self, dir_path: Optional[str] = None,
                        dir_path_key: Optional[str] = 'dir',
                        folder_name: Optional[str] = None,
                        folder_name_key: Optional[str] = None,
                        path_key: Optional[str] = 'new',
                        info_key=None) -> str:
        """The method creates the path using directory and folder name. 
        Example: final path = directory path + case_name. Here
            *   directory path can be given directly by dir_path variable or get from
            dictionary by the key dir_path_key.
        
            *   case_name can be given directly by case_name variable or get from
            dictionary by the key name_key. 

        Args:
            *   dir_path [str] is the path of directory
            *   dir_path_key [str] is the key to get dir_path from dictionary 
            *   folder name is the name of the folder
            *   folder_name_key is the key to get name of the folder from dictionary
            info_key is the key to put the prepared data to corresponding information

        Retrun: 
            None

        """
        cur_path = Priority.path(dir_path, self.info[self.get_key(info_key)]['paths'], path_key=dir_path_key)
        cur_name = Priority.name(folder_name, self.info[self.get_key(info_key)]['case_names'], name_key=folder_name_key)
        self.info[self.get_key(info_key)]['paths'][path_key] = pl.Path(cur_path) / cur_name


    def create_path(self, path, path_key='default__path_key', info_key=None):
        """
        The method creates a path in information structure. 
        Args:
            * path [pathLike] is the create path 
            path_key is the key to store the path in information structure
            info_key is the key for information structure.

        Returns:
                None
        """
        self.info[self.get_key(info_key)]['paths'][path_key] = path

    def change_path(self, new_path: str, path_key: str = 'newPath') -> None:
        """
        The method changes existing path on new path. #FIXME
        Args:
            new_path [pathLike] is the new path
            path_key [str] is the key of the existing path to be changed

        Returns:
                None
        """
        if path_key in self.info[self.info_key]['paths'].keys():
            self.info[self.info_key]['paths'][path_key] = new_path
        else:
            print('Error the key of name is not exist!')


    def get_path(self, path_key: str, info_key=None) -> str:
        """
        The function return path form info by key!
        Args:
            path_key: key for path
            info_key: key for info dictionary

        Returns:
                path corresponding to the key
        """

        return Priority.path(None, self.info[self.get_key(info_key)]['paths'], path_key=path_key)

    def set_new_parameter(self, parameter: Any,
                          info_key: Optional[str] = None,
                          parameter_name: Optional[str] = 'new_parameter'):
        """
        The method set new parameter in information structure
        Args:
            parameter is the value of the parameter
            info_key is the key of information structure
            parameter_name is the key of set parameter.

        Returns:
            None
        """
        info_key = self.get_key(info_key)
        self.info[info_key][parameter_name] = parameter

    def get_any_parameter(self, param_key: str,
                          info_key: Optional[str] = None,
                          ) -> Any:
        """
        FIXME
        Args:
            param_key:
            info_key:

        Returns:

        """
        info_key = self.get_key(info_key)
        return self.info[info_key][param_key]


    def get_key(self, key):
        """
        Проверка задания ключа. Если ключ не задан берется ключ
        из аттрибута класса
        Args:
            key:

        Returns:

        """
        if key is None:
            return list(self.info.keys())[0]
        else:
            return key

    def get_constant_path(self, case_path: str):
        """
        The method return path to constant folder being palced in case_path folder of openfoam case.

        Args:
            case_path is the path to an openfoam case.
            info_key is the key 

        Returns:
            path to constant folder

        """
        return Priority.path_add_folder(case_path, None, 'constant')

    def get_system_path(self, case_path: str, info_key: Optional[str] = None, path_key=None):
        """
         The method return path to system folder being palced in case_path folder of openfoam case.

        Args:
            case_path is the path to an openfoam case.
            info_key is the key 

        Returns:
            path to constant folder

        """
        where = self.info[self.get_key(info_key)]['paths']
        return Priority.path_add_folder(case_path, where, 'system', path_key=path_key)

    def get_any_folder_path(self, folder_name, case_path: str, info_key: Optional[str] = None):
        """
        The method returns absolute path to specify folder in case_path folder.
        EXAMPLE: 
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
        zero_path = self.get_any_folder_path('0', case_path, info_key=info_key)

        or

        zero_path = self.get_any_folder_path('0', case_path, info_key=info_key, path_key='case_path')

        Args:
            folder_name:
            case_path:
            info_key:
            folder:

        Returns:

        """
        where = self.info[self.get_key(info_key)]
        return Priority.path_add_folder(case_path, where, folder_name, path_key='case_path')

    def find_all_sif(self, folder_path: Optional[str] = None,
                     info_key: Optional[str] = None) -> list:
        """
        The method returns all files with sif extension in specify path
        Args:
            folder_path:
            info_key:

        Returns:

        """
        info_key = self.get_key(info_key)
        path_case = Priority.path(folder_path, self.info[info_key], path_key='path')

        return list(path_case.glob('**/*.sif'))

    def find_all_zero_files(self, path_case: Optional[str] = None,
                     info_key: Optional[str] = None) -> list:
        """
        The method is served to find all files in zero folder of OpenFoam case,
        for example U, p etc.
        FIXME
        Args:
            path_case: the path of openfoam case
            info_key:

        Returns:
                string
        """
        info_key = self.get_key(info_key)
        path_case = Priority.path(path_case, self.info[info_key], path_key='case_path')
        zero_folder_path = path_case / '0'
        #zero_folder_path = self.get_any_folder_path('0', path_case, info_key=info_key)
        return [file.stem for file in zero_folder_path.iterdir() if file.is_file()]

    def find_all_path_zero_files(self, path_case: Optional[str] = None,
                     info_key: Optional[str] = None) -> list:
        """
        The method is served to find all files in zero folder of OpenFoam case,
        for example U, p etc.
        FIXME
        Args:
            path_case: the path of openfoam case
            info_key:

        Returns:
                string
        """
        info_key = self.get_key(info_key)
        path_case = Priority.path(path_case, self.info[info_key], path_key='case_path')
        zero_folder_path = path_case / '0'
        #zero_folder_path = self.get_any_folder_path('0', path_case, info_key=info_key)
        return [file for file in zero_folder_path.iterdir() if file.is_file()]

    def collect_information(self, *class_set, key_info=None):
        for c_cls in class_set:
            for key, val in c_cls.info.items():
                if type(val) is not dict:
                    self.info[key] = val
                else:
                    self.info[key].update(val)

    def __init_manipulation__(self, **optional_args):

        """
        Arguments:
         * info_key: Optional[str] = 'general',
         * dir_path: Optional[str] = None
        Returns:    None

        """
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        self.info_key = info_key
        paths_dict = {'dir': self._check_type_path(optional_args.get('dir_path'))}

        self.info = {info_key: dict(paths=paths_dict,
                                    case_names={})
                     }

    def __init_elmer__(self, **optional_args):
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        case_path = self._check_type_path(optional_args.get('case_path'))
        sif_name = optional_args.get('sif_name')

        self.info = {info_key: dict(case_path=case_path,
                                    name=sif_name
                                    )}

    def __init_constant__(self, **optional_args):
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        case_path = self._check_type_path(optional_args.get('case_path'))
        self.info = {info_key: dict(case_path=case_path)}

    def __init_iv__(self, **optional_args):
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        case_path = self._check_type_path(optional_args.get('case_path'))
        self.info = {info_key: dict(case_path=case_path)}

    def __init_mesh__(self, **optional_args):
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')

        e_mesh = optional_args.get('e_mesh')
        case_path = self._check_type_path(optional_args.get('case_path'))

        self.info = {info_key: dict(case_path=case_path,
                                    elmer_mesh_name=e_mesh
                                    )}

    def __init_system__(self, **optional_args):
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        case_path = self._check_type_path(optional_args.get('case_path'))
        self.info = {info_key: dict(case_path=case_path)}

    def __init_runner__(self, **optional_args):
        """
        Optional arguments:
            case_path [PathLike or string] is the path of case to process 
            solver : [Default: pimpleFoam, str] is name of OpenFOAM solver
            mode : [Defalut: common, str] is the mode to run calculation of a model
            pyFoam : [Boolean, Default: False] in progress!
            log : [Boolean, Default: False] is the flag to save a log of calculation.
            OF_core : [int, Default: 2] is the number of cores to run openfoam case
            E_core : [int, Default: 2]  is the number of cores to run elemer case

        """
        if optional_args.get('info_key') is None:
            info_key = 'general'
        else:
            info_key = optional_args.get('info_key')
        case_path = self._check_type_path(optional_args.get('case_path'))

        OF_core = optional_args.get('OF_core', 2)
        E_core = optional_args.get('E_core', 2)
        self.info = {info_key: dict(
                                    case_path=case_path,
                                    solver=optional_args.get('solver', 'pimpleFoam'),
                                    mode=optional_args.get('mode', 'common'),
                                    pyFoam=optional_args.get('pyFoam', False),
                                    log=False,
                                    OF_core=OF_core,
                                    E_core=E_core,
                                    )
                    }

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

