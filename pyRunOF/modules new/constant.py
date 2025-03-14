from typing import Optional
import pathlib as pl
from ..additional_fun import files
from ..additional_fun.information import Information
from ..additional_fun import foamDictionaries_test as foamDict


class Constant(Information):
    """
    The class is intended to change settings of constant folder for OpenFOAM cases.
    Attributes:
        ---------------
        case_path is the path of the case to provide the manipulation with the class
        lib_path is the path of the library on your PC. The path is required only to copy files from AditionalFiles
        directory. In the future version it will be fixed.

    Methods:
        ---------------
        set_transportProp - the function sets given variables to transportProperties file
        set_any_file is the method to rewrite any variables to ant files of constant folder of OpenFOAM case.
        turbulent_model is the model to move settings of chosen turbulent models to constant folder for OpenFOAM case.
        turbulent_model_old is the old version of above method.
        test
    """

    def __init__(self, **optional_args):
        Information.__init_constant__(self, **optional_args)


    def set_items(self, file, *lists: dict, **options):
        """The function sets given variables to chosen file in constant folder
        Arguments:
            * *lists [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key to get path from dictionary of paths of Information class

        Return: None
        """
        case_path = options.get('case_path')
        info_key = options.get('info_key')
        constant_path = self.get_constant_path(case_path, info_key=self.get_key(info_key))
        rel_path = constant_path / file
        merged_dict = {}
        for cur_dict in lists:
            merged_dict.update(cur_dict)
        foamDict.set_foamDict_value(merged_dict, case_path, rel_path)



    def set_transportProp(self, *lists: dict, **options) -> None:
        """The function sets given variables to transportProperties file
        Arguments:
            * *lists [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key to get path from dictionary of paths of Information class
        Return: None
        """
        case_path = options.get('case_path')
        info_key = options.get('info_key')
        constant_path = self.get_constant_path(case_path, info_key=self.get_key(info_key))
        for dict_var in lists:
            for name_var, value_var in dict_var.items():
                files.change_var_fun(name_var, value_var, constant_path, 'transportProperties')




    def set_any_file(self, *lists_var: dict, files: list = ['transportProperties'],
                     **options) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase

        Arguments:

            * *lists [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * files [list of strings] is the list with names of files in constant folder where
            variables will be being found.
            * **options are the optional arguments. The set of avaible settings are listed below
                    * case_path [str] is the case path with transportProp file
                    * info_key [str] is the key to get path from dictionary of paths of Information class

        Return: None
        """
        case_path = options.get('case_path')
        info_key = options.get('info_key')
        constant_path = self.get_constant_path(case_path, info_key=self.get_key(info_key))
        for file_name in files:
            for dict_var in lists_var:
                for name_var, value_var in dict_var.items():
                    files.change_var_fun(name_var, value_var, constant_path, file_name)

    def turbulent_model(self, **options):
        """"The fucntion serves to set required turbulent model for solving task. For this purpose, one of list
          of wrriten files with given settings will be renamed into turbulenceProperties to system folder of adjusted case
        acording required type of rubulence model
        
        Arguments: 

        **options are the optional arguments. The set of avaible settings are listed below
        * case_path [str] is the case path with turbulenceProperties file 
        * info_key [str] is the key to get path from dictionary of paths of Information clas
        * turbulent_type is the string describing type of turbulence model. At the current version of
        PyRunOF the avaible models are listed bellow
            * 'laminar' is the default model
            * 'LES' 
            * 'kEpsilon'
            * 'realizablekE'
            * 'kOmega'
            * 'kOmegaSST'
            * 'laminar'
            * 'LESdynamicSmag'

        Return: None
                """
        case_path = options.get('case_path')
        info_key = options.get('info_key')
        constant_path = self.get_constant_path(case_path, info_key=self.get_key(info_key))

        lib_path = pl.Path(__file__).parents[1]
        
        turbulent_files_path = lib_path / 'files' / 'TurbulenceFiles'
        turbulent_type = options.get('turbulent_type', 'laminar')
        files.copy_file(turbulent_files_path, constant_path,
                        f'turbulenceProperties_{turbulent_type}', 'turbulenceProperties')


    def set_parameter(self, *lists_var: dict, files: list = ['controlDict'],
                     **options) -> None:
        case_path = options.get('case_path')
        info_key = options.get('info_key')
        system_path = self.get_system_path(case_path, self.get_key(info_key))

        for file_name in files:
            for dict_var in lists_var:
                foamDict.set_foamDict_value(dict_var, case_path, f'constant/{file_name}')