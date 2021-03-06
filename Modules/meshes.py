import os
from Modules.auxiliary_functions import Priority, Files, Executer
from typing import List, Optional, Dict
from Modules.information import Information


class Mesh(Information):
    """
    The class is intended to perform operations on OpenFOAM and Elmer_old meshes.
    Attributes
        ----------
        case_path is the path_dict of the case required providing manipulations with meshes
        elmer_mesh_nam is the name of Elmer_old mesh folder
    Methods
        -------
        set_blockMesh is the method to set parameters for blockMesh utility implemented in OpenFOAM to
        build mesh. The settings of the utility is stored in blockMesh file in system folder of your OpenFOAM case
        run_blockMesh is the method to run meshBlock utility for the chosen case.
        run_gMesh_to_Elmer is the method to transforms gmsh format of mesh (.geo) to Elmer_old mesh.
        set_gMesh si the method to set parameters in geo file of the mesh for gMesh software.
    """

    def __init__(self, info_key: Optional[str] = 'general',
                       case_path: Optional[str] = None,
                       elmer_mesh_name: Optional[str] = None):
        """PathCase is name where the class will be doing any manipulation"""
        Information.__init_mesh__(info_key=info_key, case_path=case_path, elmer_mesh_name=elmer_mesh_name)

    def set_blockMesh(self, mesh_var_dict: dict, var_key: Optional[str] = None,
                      case_path: Optional[str] = None) -> None:
        """The method to set given parameters in blockMeshDict files for blockMesh utility.
        The general idea of the method is to find given part of text in blockMeshDict file and to change
        the part of text on given value. You have to set the flags, keys of mesh_var_dict,
        in the blockMeshDict yourselves for purpose of the method can find them and change it.
        It should be noted the flag to be unique.
        Input :
            mesh_var_dict is the dictionary consist of keys as name of variables or other words flags
            in blockMeshDict and its values for change of the given flags to the corresponding value.
            case_path is the path_dict of case where you want to tune blockMesh utility. If the variable is None,
            then the variable is taken from attributes of the object.
        Output:
            None

        """
        case_path = Priority.path(case_path, self.info, path_key='path')
        system_path = case_path / 'system'
        mesh_var_dict = Priority.variable(mesh_var_dict, self.info, var_key=var_key)
        for var in mesh_var_dict:
            Files.change_var_fun(var, mesh_var_dict[var], path=system_path,
                                 file_name='blockMeshDict')

    def run_blockMesh(self, case_path: Optional[str] = None) -> None:
        """The method to execute blockMesh utility of OpenFOAM in the given case.
            Input :
                case_path is the path_dict for running of blockMesh utility.
                If the path_dict is None, then the variable is taken from attributes of the object.
            Output:
                    None

        """
        case_path = Priority.path(case_path, self.info, path_key='path')
        Executer.run_command('blockMesh', case_path)

    def run_gMesh_to_Elmer(self, case_path: Optional[str] = None,
                           elmer_mesh_name: Optional[str] = None) -> None:
        """The method to execute a number of commands to transform mesh from gMesh extension to Elmer_old one.
            Input :
                case_path is the path_dict for running of these commands .
                If the path_dict is None, then the variable is taken from attributes of the object.
            Output:
                    None

        """
        case_path = Priority.path(case_path, self.info, path_key='path')
        elmer_mesh_name = Priority.variable(elmer_mesh_name, self.info, var_key='elmer_mesh_name')
        command1 = f'gmsh -3 {elmer_mesh_name}.geo'
        command2 = f'ElmerGrid 14 2 {elmer_mesh_name} -autoclean '
        Executer.run_command(command1, case_path)
        Executer.run_command(command2, case_path)

    def set_gMesh(self, mesh_var_dict: dict, case_path: Optional[str] = None, mesh_name: str = '', var_key=None) -> None:
        """The method to set given parameters in the file with geo extension.
        The general idea of the method is to find given part of text in gMesh file and to change
        the part of text on given value. You have to set the flags, keys of mesh_var_dict,
        in the geo file yourselves for purpose of the method can find them and change it.
        It should be noted the flag to be unique.
            Input :
                mesh_var_dict is the dictionary consist of keys as name of variables or other words flags
                in the geo file and its values for change of the given flags to the corresponding value.
                case_path is the path_dict of case where you want to tune gMesh utility. If the variable is None,
                then the variable is taken from attributes of the object.
                mesh_name is the string representing name of geo file without .geo extension.
            Output:
                    None

        """
        case_path = Priority.path(case_path, self.info, path_key='path')
        elmer_mesh_name = Priority.variable(mesh_name, self.info, var_key='elmer_mesh_name')
        mesh_var_dict = Priority.variable(mesh_var_dict, self.info, var_key=var_key)
        for var in mesh_var_dict:
            Files.change_var_fun(var, mesh_var_dict[var], case_path, file_name=f'{elmer_mesh_name}.geo')
