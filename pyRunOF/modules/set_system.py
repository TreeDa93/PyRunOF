from typing import List, Optional
from ..additional_fun.auxiliary_functions import Files
from ..additional_fun.information import Information

class System(Information):
    """
    The class is supported for processing the system file of openfoam cases. 

    Methods:
         
        * set_control_dict is the method to set require values in controlDict file of openfoam cases.

        * set_fvSolution is the method to set require values in fvSolution file of openfoam cases.

        * set_fvSchemes is the method to set require values in fvSchmes file of openfoam cases.

        * set_any_files is the method to set require values in any files of openfoam cases in system folder.

    """

    def __init__(self, **optional_args) -> None:
        """
        Args:
            **optional_args:
                * info_key
                * case_path
        """
        Information.__init_system__(self, **optional_args)
   

    def set_controlDict(self, *lists: dict, **options) -> None:
        """The function sets given variables to controlDict file
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
        system_path = self.get_system_path(case_path, info_key=self.get_key(info_key))
        for dict_var in lists:
            for name_var, value_var in dict_var.items():
                Files.change_var_fun(name_var, value_var, system_path, 'controlDict')

   
    def set_fvSolution(self, *lists: dict, **options) -> None:
        """The function sets given variables to fvSolution file
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
        system_path = self.get_system_path(case_path, info_key=self.get_key(info_key))
        for dict_var in lists:
            for name_var, value_var in dict_var.items():
                Files.change_var_fun(name_var, value_var, system_path, 'fvSolution')


    def set_fvSchemes(self, *lists: dict, **options) -> None:
        """The function sets given variables to fvSchemes file
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
        system_path = self.get_system_path(case_path, info_key=self.get_key(info_key))
        for dict_var in lists:
            for name_var, value_var in dict_var.items():
                Files.change_var_fun(name_var, value_var, system_path, 'fvSchemes')


    def set_any_file(self, *lists_var: dict, files: list = ['controlDict'],
                     **options) -> None:
        """The function sets given variables to given files of system folder

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
        system_path = self.get_system_path(case_path, self.get_key(info_key))
        
        for file_name in files:
            for dict_var in lists_var:
                for name_var, value_var in dict_var.items():
                    Files.change_var_fun(name_var, value_var, system_path, file_name)
