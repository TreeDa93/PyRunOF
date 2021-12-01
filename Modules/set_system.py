import os
import sys
from Modules.auxiliary_functions import change_var_fun
from Modules.auxiliary_functions import Priority
from Modules.auxiliary_functions import Files

class SetSystem:
    """
    #FIXIT

    """

    def __init__(self, case_path=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.case_path = case_path
        if case_path is None:
            self.system_path = case_path
        else:
            self.system_path = os.path.join(case_path, 'system')

    def set_control_dict(self, *lists_controlDicts, case_path=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""

        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in lists_controlDicts:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], case_path=system_path,
                                     file_name='controlDict')

    def set_fvSolution(self, *listsfvSolution, case_path=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in listsfvSolution:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], case_path=system_path,
                                     file_name='fvSolution')

    def set_fvSchemes(self, *listsfvSchemes, case_path=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in listsfvSchemes:
            for var in list_var:
                Files.change_var_fun(var, list_var[var], case_path=system_path,
                                     file_name='fvSchemes')

    def set_any_files(self, *listsVar, files=['controlDict'], case_path=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for file in files:
            for list_var in listsVar:
                for var in list_var:
                    Files.change_var_fun(var, list_var[var], case_path=system_path,
                                         file_name=file)

    def set_end_time(self, new_end_time, case_path="./"):
        controlDict_path = case_path + "/system/controlDict"
        output_file = open(controlDict_path + "_temp", 'w')
        with open(controlDict_path, 'r') as input_file:
            for line in input_file:
                if ("endTime" in line) and ("stopAt" not in line):
                    time_value = line.split()[1]
                    new_line = line.replace(time_value, str(new_end_time) + ";")
                    output_file.write(new_line)
                else:
                    output_file.write(line)
        output_file.close()
        os.system("mv " + controlDict_path + "_temp " + controlDict_path)
        return


    def set_control_dict_test(self, *lists_controlDicts, case_path=None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""

        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for list_var in lists_controlDicts:
            for var in list_var:
                Files.change_text_line(var, list_var[var], 'stopAt', path=system_path,
                                     file_name='controlDict')