import os
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict


class Mesh:
    """
    The class is intended to perform operations on OpenFOAM and Elmer meshes.
    Attributes
        ----------
        case_path is the path_dict of the case required providing manipulations with meshes
        elmer_mesh_nam is the name of Elmer mesh folder
    Methods
        -------
        set_blockMesh is the method to set parameters for blockMesh utility implemented in OpenFOAM to
        build mesh. The settings of the utility is stored in blockMesh file in system folder of your OpenFOAM case
        run_blockMesh is the method to run meshBlock utility for the chosen case.
        run_gMesh_to_Elmer is the method to transforms gmsh format of mesh (.geo) to Elmer mesh.
        set_gMesh si the method to set parameters in geo file of the mesh for gMesh software.
    """

    def __init__(self, case_path=None):
        """PathCase is name where the class will be doing any manipulation"""
        self.case_path = case_path
        self.elmer_mesh_name = ''
        #self.info = {}

    def set_blockMesh(self, mesh_var_dict: dict, case_path: Optional[str] = None) -> None:
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
        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')  # system folder path_dict
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
        case_path = Priority.path(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path_dict
        os.chdir(case_path)
        os.system('blockMesh')
        os.chdir(curr_path)

    def run_gMesh_to_Elmer(self, case_path: Optional[str] = None) -> None:
        """The method to execute a number of commands to transform mesh from gMesh extension to Elmer one.
            Input :
                case_path is the path_dict for running of these commands .
                If the path_dict is None, then the variable is taken from attributes of the object.
            Output:
                    None

        """
        case_path = Priority.path(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path_dict
        os.chdir(case_path)
        os.system(f'gmsh -3 {self.elmer_mesh_name}.geo')
        os.system(f'ElmerGrid 14 2 {self.elmer_mesh_name} -autoclean ')
        os.chdir(curr_path)

    def set_gMesh(self, mesh_var_dict: dict, case_path: Optional[str] = None, mesh_name: str = '') -> None:
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
        case_path = Priority.path(case_path, None, self.case_path)
        os.chdir(case_path)
        self.elmer_mesh_name = mesh_name
        for var in mesh_var_dict:
            Files.change_var_fun(var, mesh_var_dict[var], case_path, file_name=f'{self.elmer_mesh_name}.geo')


class Mesh_new:
    """
    The class is intended to perform operations on OpenFOAM and Elmer meshes.
    Attributes
        ----------
        case_path is the path_dict of the case required providing manipulations with meshes
        elmer_mesh_nam is the name of Elmer mesh folder
    Methods
        -------
        set_blockMesh is the method to set parameters for blockMesh utility implemented in OpenFOAM to
        build mesh. The settings of the utility is stored in blockMesh file in system folder of your OpenFOAM case
        run_blockMesh is the method to run meshBlock utility for the chosen case.
        run_gMesh_to_Elmer is the method to transforms gmsh format of mesh (.geo) to Elmer mesh.
        set_gMesh si the method to set parameters in geo file of the mesh for gMesh software.
    """

    def __init__(self, case_path: Optional[str] = None,
                 elmer_mesh_name: Optional[str] = None,
                 key: Optional[str] = 'general') -> None:
        """PathCase is name where the class will be doing any manipulation"""
        self.info = dict.fromkeys([key], dict(path=case_path,
                                              name=elmer_mesh_name))
        self.general_key = key

    def set_blockMesh(self, mesh_var_dict: dict, case_path: Optional[str] = None) -> None:
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
        case_path = Priority.path(case_path, None, self.case_path)
        system_path = os.path.join(case_path, 'system')  # system folder path_dict
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
        case_path = Priority.path(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path_dict
        os.chdir(case_path)
        os.system('blockMesh')
        os.chdir(curr_path)

    def run_gMesh_to_Elmer(self, case_path: Optional[str] = None) -> None:
        """The method to execute a number of commands to transform mesh from gMesh extension to Elmer one.
            Input :
                case_path is the path_dict for running of these commands .
                If the path_dict is None, then the variable is taken from attributes of the object.
            Output:
                    None

        """
        case_path = Priority.path(case_path, None, self.case_path)
        curr_path = os.getcwd()  # current path_dict
        os.chdir(case_path)
        os.system(f'gmsh -3 {self.elmer_mesh_name}.geo')
        os.system(f'ElmerGrid 14 2 {self.elmer_mesh_name} -autoclean ')
        os.chdir(curr_path)

    def set_gMesh(self, mesh_var_dict: dict, case_path: Optional[str] = None, mesh_name: str = '') -> None:
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
        case_path = Priority.path(case_path, None, self.case_path)
        os.chdir(case_path)
        self.elmer_mesh_name = mesh_name
        for var in mesh_var_dict:
            Files.change_var_fun(var, mesh_var_dict[var], case_path, file_name=f'{self.elmer_mesh_name}.geo')
