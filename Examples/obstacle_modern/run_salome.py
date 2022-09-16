import os
import sys
libpath = '/home/ivan/PyRunOF/' #write path to pyRunOF library
sys.path.append(libpath)  # add the library into system pathes
from Modules.auxiliary_functions import Executer

Executer.run_command('salome', os.getcwd())
