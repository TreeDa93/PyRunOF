from typing import List, Optional
from ..additional_fun.auxiliary_functions import Files
from ..additional_fun.information import Information

class System(Information):
    """
    The class is supported for processing the system file of openfoam cases. 

    Methods:
         
         set_control_dict is the method to set require values in controlDict file of openfoam cases.

         set_fvSolution is the method to set require values in fvSolution file of openfoam cases.

         set_fvSchemes is the method to set require values in fvSchmes file of openfoam cases.

         set_any_files is the method to set require values in any files of openfoam cases in system folder.

    """

    def __init__(self, info_key: Optional[str] = 'general', case_path: Optional[str] = None) -> None:
        """PathCase is name where the class will be doing any manipulation"""
        Information.__init_system__(self, info_key=info_key, case_path=case_path)

    def set_control_dict(self, *lists: dict, case_path: Optional[str] = None, info_key: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        system_path = self.get_system_path(case_path, self.get_key(info_key))
        for dict_var in lists:
            for var in dict_var:
                Files.change_var_fun(var, dict_var[var], path=system_path,
                                     file_name='controlDict')

    def set_fvSolution(self, *listsfvSolution: dict, case_path: Optional[str] = None, info_key: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        system_path = self.get_system_path(case_path, self.get_key(info_key))
        for list_var in listsfvSolution:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], path=system_path,
                                     file_name='fvSolution')

    def set_fvSchemes(self, *listsfvSchemes: dict, case_path: Optional[str] = None, info_key: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        system_path = self.get_system_path(case_path, self.get_key(info_key))
        for list_var in listsfvSchemes:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], path=system_path,
                                     file_name='fvSchemes')

    def set_any_files(self, *listsVar: dict, files: List[str] = ['controlDict'],
                      case_path: Optional[str] = None, info_key: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        system_path = self.get_system_path(case_path, self.get_key(info_key))
        for file in files:
            for list_var in listsVar:
                for var in list_var:
                    Files.change_var_fun(var, list_var[var], path=system_path,
                                         file_name=file)
