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
                       e_mesh: Optional[str] = None):
        """PathCase is name where the class will be doing any manipulation"""
        Information.__init_mesh__(self, info_key=info_key,
                                  case_path=case_path,
                                  e_mesh=e_mesh)

    def set_blockMesh(self, mesh_var_dict: dict, var_key: Optional[str] = None,
                      case_path: Optional[str] = None, info_key=None) -> None:
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
        system_path = self.get_system_path(case_path, info_key=info_key)
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

    def set_decomposePar(self, *mesh_dicts: dict, case_path: Optional[str] = None,
                         info_key: Optional[str]= None) -> None:
        """
        The method complete decimposeParDict file in system folder of openfoam case according input data.
        Input :
            mesh_dicts is the dictionary containing of key as variable to be replaced in decimposeParDict file and
                            values as digs to be filled instead of key in decimposeParDict file
            case_path is path where the manipulation will do.

            info_key is key of information.
        Output:
            None

        """
        system_path = self.get_system_path(case_path, info_key=info_key)
        for mesh_dict in mesh_dicts:
            for var in mesh_dict:
                    Files.change_var_fun(var, mesh_dict[var], path=system_path,
                                         file_name='decomposeParDict')



    def decompose_run_OF(self, case_path=None, info_key=None):
        """
        запуск  #FIXME
        """
        path_case = self.get_path(case_path=case_path, info_key=self.get_key(info_key))
        command = 'decomposePar -force'
        Executer.run_command(command, path_case)

    def decompose_run_Elmer(self, path, info_key=None):
        """
                запуск #FIXME
        """
        path_case = self.get_path(case_path=path, info_key=self.get_key(info_key))
        mesh_name = self.get_any_parameter(parameter_name='e_mesh', info_key=info_key)
        cores = self.get_any_parameter(parameter_name='e_cores', info_key=info_key)
        command = f'ElmerGrid 2 2 {mesh_name} -metis {cores} -force'
        Executer.run_command(command, path_case)

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


    def run_salome_mesh(self, script_path: Optional[str] = None, parameter_path: Optional[str] = None,
                          info_key: Optional[str]=None):
        """
        The method creates salome mesh from salome scripts
        script_path
        parameters_path
        """
        script_path = Priority.path(script_path, self.info, info_key)
        script_name = script_path.stem
        where = script_path.parent
        parameter_path = Priority.path(parameter_path, self.info, info_key)

        command = f"salome -t {script_name} args:{parameter_path}"
        Executer.run_command(command, where)


    def change_salomeMesh(self, parameters_path: Optional[str] = None, changed_parameters: Optional[dict] = None,
                          new_path: Optional[str] = None):
        """
        The method changes mesh parameters and return path to new parameters
        parameters_path path to origin parameters json file
        changed_parameters dictionary filled with parameters to change
        new_path full path to changed json file if it's None, then origin file will be rewritten
        """
        parameters = Files.open_json(parameters_path)

        for key, value in parameters.items():
            parameters[key] = changed_parameters.get(key, value)
        if new_path:
            Files.save_json(parameters, new_path)
        else:
            Files.save_json(parameters, parameters_path)

