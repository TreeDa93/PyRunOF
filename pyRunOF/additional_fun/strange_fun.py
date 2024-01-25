import  pathlib as pl
from auxiliary_functions import Files
import subprocess
import sys

def change_text_line(var_value: any, var_name: any, var_excl_name: any,
                     path: str = None, file_name: str = '') -> None:
    """ The function is served to find the variable named var_name in th file_name
    which has directory path_dict. If the variable has been founded and
    variable var_excl_name does not exist in the line then the value of the variable
    is changed by var_value
    Attributes:
    --------------
            var_value [string or numbers] is the value to be written instead var_name

            var_name depicts place in the given file where should be written var_value

            var_excl_name is the name to be absented in the text line in order to change founded variable var_name.

            path_dict is the path_dict with the required file for searching of given variable.

            file_name is the name of the file  where the method will fulfil searching.
    """
    path = pl.Path(path) / file_name  # -> path = os.path.join(path, file_name)
    new_data = ''
    with path.open(mode='r') as f:
        for line in f:
            if (var_name in line) and (var_excl_name not in line):
                new_data += f'{var_name} \t\t {var_value}; \n'
            else:
                new_data += line
    with path.open(mode='w') as f:
        f.write(new_data)



# from Priority


def file(self, file):
    """The method is used for selection of given name
    the first priority is given name by methods
    the second priority is given name by class constructor
    If both name is None, the program is interupted
    Input :
    basePath, newPath is checkoing pathes
    Output:
    retrunBasePath, returnNewPath is selected pathes acording priority
    """
    if file is None:
        if self.file is not None:
            return self.file
        else:
            sys.exit('Error: You do not enter the name of the file!!!')
    else:
        return file
