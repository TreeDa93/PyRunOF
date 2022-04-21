import os
from Modules.auxiliary_functions import Priority
from Modules.auxiliary_functions import Files
from typing import List, Optional, Dict


class System:
    """
    #FIXME

    """

    def __init__(self, case_path: Optional[str] = None) -> None:
        """PathCase is name where the class will be doing any manipulation"""
        self.case_path = case_path
        if case_path is None:
            self.system_path = case_path
        else:
            self.system_path = os.path.join(case_path, 'system')

    def set_control_dict(self, var_dict: dict, case_path: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""

        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for var in var_dict:
            Files.change_var_fun(var, var_dict[var], path=system_path,
                                 file_name='controlDict')

    def set_control_dict2(self, var_dict: dict, excl_dict: dict, case_path: Optional[str] = None) -> None:
        """Функция ищет заданную переменную в строчке var_dict
        var_dict = {var_name: value of the variable}
        excl_dict = {var_name: str} - str sholde be exclude in the line
        """

        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for var_name in var_dict:
            Files.change_text_line(var_dict[var_name], var_name, excl_dict[var_name], path=system_path,
                                   file_name='controlDict')

    def set_fvSolution(self, *listsfvSolution: dict, case_path: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in listsfvSolution:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], path=system_path,
                                     file_name='fvSolution')

    def set_fvSchemes(self, *listsfvSchemes: dict, case_path: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in listsfvSchemes:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], path=system_path,
                                     file_name='fvSchemes')

    def set_any_files(self, *listsVar: dict, files: List[str] = ['controlDict'],
                      case_path: Optional[str] = None) -> None:
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for file in files:
            for list_var in listsVar:
                for var in list_var:
                    Files.change_var_fun(var, list_var[var], path=system_path,
                                         file_name=file)


