import os
from Modules.auxiliary_functions import Files, Priority


class Constant:
    """
    The class is intended to change settings of constant folder for OpenFOAM cases.
    Attributes:
        ---------------
        case_path is the path of the case to provide the manipulation with the class
        lib_path is the path of the library on your PC. The path is required only to copy files from AditionalFiles
        directory. In the future version it will be fixed.

    Methods:
        ---------------
        set_transportProp - the the function sets given variables to transportProperties file
        set_any_file is the method to rewrite any variables to ant files of constant folder of OpenFOAM case.
        turbulent_model is the model to move settings of chosen turbulent models to constant folder for OpenFOAM case.
        turbulent_model_old is the old version of above method.
    """

    def __init__(self, case_path: str = None, lib_path: str = None):
        self.case_path = case_path
        self.lib_path = lib_path

    def set_transportProp(self, *lists: dict, case_path=None) -> None:
        """The function sets given variables to transportProperties file
        patheNewCase is the name where transportProperties will be modificated
        lists are a number of dictionaries with keys, which called as name of variables to transportProperties,
        and values"""
        path = Priority.path(case_path, None, self.case_path)
        constant_path = os.path.join(path, 'constant')
        for dict_var in lists:
            for var in dict_var:
                Files.change_var_fun(var, dict_var[var], path=constant_path, file_name='transportProperties')

    def set_any_file(self, *lists_var: dict, files: list[str] = ['controlDict'], case_path: str = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        path = Priority.path(case_path, None, self.case_path)
        constant_path = os.path.join(path, 'constant')
        for file_name in files:
            for dict_var in lists_var:
                for var in dict_var:
                    Files.change_var_fun(var, dict_var[var], path=constant_path, file_name=file_name)

    def turbulent_model(self, turbulent_type='kEpsilon', case_path=None, lib_path=None, add_file_path=None):
        """"The fucntion serves to set required turbulent model for solving task. For this purpose, one of list
          of wrriten files with given settings will be renamed into turbulenceProperties to system folder of adjusted case
        acording required type of rubulence model
        path_new_case is the name of the new case
        turbulent_type is variables definding type of turbulence model
                LES
                kEpsilon
                realizablekE
                kOmega
                kOmegaSST
                laminar
                LESSmag
                your_any ...
                """
        case_path = Priority.path(case_path, None, self.case_path)
        constant_path = os.path.join(case_path, 'constant')
        if add_file_path is None:
            lib_path = Priority.path(lib_path, None, self.lib_path)
            turbulent_files_path = os.path.join(lib_path, 'AdditinalFiles', 'TurbulenceFiles')
        Files.copy_file(turbulent_files_path, constant_path,
                        old_name=f'turbulenceProperties_{turbulent_type}', new_name='turbulenceProperties')

    def turbulent_model_old(self, turbulent_type='kEpsilon', case_path=None):
        """"The fucntion serves to set required turbulent model for solving task. For this purpose, one of list
          of wrriten files with given settings will be renamed into turbulenceProperties to system folder of adjusted case
        acording required type of rubulence model
        path_new_case is the name of the new case
        turbulent_type is variables definding type of turbulence model
                LES
                kEpsilon
                realizableKE
                kOmega
                kOmegaSST
                """
        case_path = Priority.path(case_path, None, self.case_path)
        constant_path = os.path.join(case_path, 'constant')
        Files.copy_file(constant_path, constant_path,
                        old_name=f'turbulenceProperties_{turbulent_type}', new_name='turbulenceProperties')

