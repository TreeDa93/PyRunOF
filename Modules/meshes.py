import os
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict


class Mesh:
    """
    FIXME

    """

    def __init__(self, case_path=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.case_path = case_path
        self.elmer_mesh_name = ''

    def set_blockMesh(self, mesh_list: List, case_path: Optional[str] = None) -> None:
        """The fucntion sets given variables to blockMeshDict file
        meshList is the dictionary with variables and name of the variables, which will be set at blockMeshDict file
        """
        case_path = Priority.path2(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')
        for var in mesh_list:
            Files.change_var_fun(var, mesh_list[var], path=system_path,
                                 file_name='blockMeshDict')

    def run_blockMesh(self, case_path: Optional[str] = None) -> None:
        """The function creates mesh by blockMesh OpenFOAM utilite"""

        case_path = Priority.path2(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path
        os.chdir(case_path)
        os.system('blockMesh')
        os.chdir(curr_path)

    def run_gMesh_to_Elmer(self, case_path: Optional[str] = None) -> None:
        case_path = Priority.path2(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path
        os.chdir(case_path)
        os.system(f'gmsh -3 {self.elmer_mesh_name}.geo')
        os.system(f'ElmerGrid 14 2 {self.elmer_mesh_name} -autoclean ')
        os.chdir(curr_path)

    def set_gMesh(self, mesh_list: List, case_path: Optional[str] = None, mesh_name: str = '') -> None:
        case_path = Priority.path2(case_path, None, self.case_path)
        os.chdir(case_path)
        self.elmer_mesh_name = mesh_name
        for var in mesh_list:
            Files.change_var_fun(var, mesh_list[var], case_path, file_name=f'{self.elmer_mesh_name}.geo')
