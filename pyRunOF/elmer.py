from typing import Optional
from .auxiliary_functions import Priority, Files
from .information import Information


class Elmer(Information):
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
        Information.__init_elmer__(info_key=key, case_path=case_path,
                                   sif_name=sif_name)

    def set_var(self, *elmer_dicts: dict,
                case_path: Optional[str] = None,
                sif_name: Optional[str] = None,
                info_key: Optional[str] = None,
                var_key: Optional[str] = None):
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
        info_key = self.get_key(info_key)
        case_path = Priority.path(case_path, self.info[info_key], path_key='path')
        sif_name = Priority.name(sif_name, self.info[info_key], name_key='name')
        sif_name = self._check_prefix_sif(sif_name)
        elmer_dicts = Priority.variable(elmer_dicts, self.info, var_key=var_key)
        if elmer_dicts is not list():
            elmer_dicts = list(elmer_dicts)
        for elmer_dict in elmer_dicts:
            for var in elmer_dict:
                Files.change_var_fun(var, elmer_dict[var], path=case_path, file_name=sif_name)

    def set_var_by_line(self):
        """
        FIXME
        """
        pass


class Elmer_old:
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
        path_case = Priority.path(path_case, self.path_case)
        sif_name = Priority.name(sif_name, self.sif_name)
        if '.sif' not in sif_name:
            sif_name += '.sif'
        for elmer_dict in elmer_dicts:
            for var in elmer_dict:
                Files.change_var_fun(var, elmer_dict[var], path=path_case, file_name=sif_name)

    def set_elmer_case(self, sif_name: str = None, path_case: str = None):
        sif_name = Priority.name(sif_name, None, self.sif_name)
        if '.sif' not in sif_name:
            sif_name += '.sif'

    def set_elmer_path(self, sif_name: str = None, path_case: str = None):
        sif_name = Priority.name(sif_name, None, self.sif_name)
        if '.sif' not in sif_name:
            sif_name += '.sif'
