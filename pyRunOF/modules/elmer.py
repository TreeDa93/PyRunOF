from typing import Optional
from ..additional_fun.auxiliary_functions import Files, Priority
from ..additional_fun.information import Information

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

    def set_var(self, *elmer_dicts, **options):
        """The function sets given variables to sif file of Elemer
        Arguments:

            * *elmer_dicts is a set of dictionaries with keys as names or flags of variable in sif file
            * **options:
                * case_path: Optional[str] = None,
                * sif_name: Optional[str] = None,
                * info_key: Optional[str] = None

        Return: None

        """
        info_key = self.get_key(options.get('info_key'))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='path')
        
        sif_name = Priority.name(options.get('sif_name'), self.info[info_key], name_key='name')
        sif_name = self._check_prefix_sif(sif_name)
        
        for elmer_dict in elmer_dicts:
            for var_name, value_var in elmer_dict.items():
                Files.change_var_fun(var_name, value_var, case_path, sif_name)

