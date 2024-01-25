from typing import Optional
from ..additional_fun.auxiliary_functions import Priority, Files, run_command
from ..additional_fun.information import Information

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

    def __init__(self, **optional_args):
        """
        Args:
            **optional_args:
                * info_key: Optional[str] = 'general',
                * case_path: Optional[str] = None,
                * e_mesh: Optional[str] = None
        """
        Information.__init_mesh__(self, **optional_args)

    def set_blockMesh(self, *mesh_dicts: dict, **options) -> None:
        """The function sets given variables to blockMeshDict file
        
        Arguments:

            * *mesh_dicts [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key to get path from dictionary of paths of Information class
        
        Return: None
        """
        info_key = self.get_key(options.get('info_key'))
        
        system_path = self.get_system_path(options.get('case_path'), info_key=info_key)

        for mesh_dict in mesh_dicts:
            for var_name, value_var in mesh_dict.items():
                Files.change_var_fun(var_name, value_var, system_path, 'blockMeshDict')


    

    def set_decomposePar(self, *mesh_dicts: dict, **options) -> None:
        """The function sets given variables to decomposePar file
        
        Arguments:

            * *mesh_dicts [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key to get path from dictionary of paths of Information class
        
        Return: None
        """
        info_key = self.get_key(options.get('info_key'))
        
        system_path = self.get_system_path(options.get('case_path'), info_key=info_key)

        for mesh_dict in mesh_dicts:
            for var_name, value_var in mesh_dict.items():
                Files.change_var_fun(var_name, value_var, system_path, 'decomposeParDict')

    def set_gmseh(self, *mesh_dicts: dict, **options) -> None:
        """The function sets given variables to gmesh file
        
        Arguments:

            * *mesh_dicts [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key to get path from dictionary of paths of Information class
                * info_key_mesh is the key of dictionary with value name of gmesh file.
        
        Return: None
        """
        info_key = self.get_key(options.get('info_key'))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')

        mesh_name = options.get('mesh_name')
        info_key_mesh = options.get('info_key_mesh', 'e_mesh')
        mesh_name = Priority.variable(mesh_name, self.info, info_key_mesh)
        
        
        for mesh_dict in mesh_dicts:
            for var_name, value_var in mesh_dict.items():
                Files.change_var_fun(var_name, value_var, case_path, f'{mesh_name}.geo')


    def run_blockMesh(self, **options) -> None:
        """The method to execute blockMesh utility of OpenFOAM in the given case.
            
            Arguments :
            * **options are the optional arguments. The set of avaible settings are listed below
                * info_key [str] is the key to get path from dictionary of paths of Information class
                * case_path [str] is the case path with transportProp file

            Return: None

        """

        info_key = self.get_key(options.get('info_key'))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
        run_command('blockMesh', case_path)

    def run_salome_mesh(self, **options):
        info_key = self.get_key(options.get('info_key'))
        path_key = options.get('key_script_path')
        script_path = Priority.path(options.get('script_path'), self.info[info_key], path_key=path_key)

        parameter_path = Priority.path(options.get('parameter_path'), self.info[info_key],
                                       options.get('key_parameter_path'))

        script_name = script_path.stem
        script_root_path = script_path.parent

        command = f"salome -t {script_name} args:{parameter_path}"
        run_command(command, script_root_path)

    def run_decompose(self, what='OF', **options):
        """The function run decompose procedure for OpenFOAM or Elmer depending on what flag.
        
        Arguments:

            * *mesh_dicts [list of dicts] is the set of dictionaries. The keys of the dictionaries are
            the desired varible in trasportProp, which will be changed to the value taken from 
            the dictionary corresponding the specified key. 
            * **options are the optional arguments. The set of avaible settings are listed below
                to run openfoam
                * case_path [str] is the case path with transportProp file
                * info_key [str] is the key of dictionary with parameters from Information class
                to run Elmer It is requried do add two settings
                * info_key_mesh [str] is the key to get Elemer mesh name from dictionary of paths of Information class
                * info_key_cores [str] is the key to get the numer of cores for Elmer from dictionary of paths of Information class
                to run salome script 
                * script_path is the python script to run salome building
                * parameter_path is the input parameters for salome python script.
                to run gmesh 
                * mesh_name is the name of gmesh file with geo extension.
                or
                * key_mesh_name us the key of dictionary where the name of gmesh file is stored. 
        
        Return: None
        """
        info_key = self.get_key(options.get('info_key'))
        match what:
            case 'OF' | 'OpenFOAM' | 'openfoam':

                case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')

                command = 'decomposePar -force'
                run_command(command, case_path)
            case 'elmer' | 'Elmer':
                info_key = self.get_key(options.get('info_key'))
                case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
                
                mesh_name = options.get('mesh_name')
                info_key_mesh = options.get('info_key_mesh')
                mesh_name = Priority.variable(mesh_name, self.info[info_key], info_key_mesh)

                cores = options.get('cores')
                info_key_cores = options.get('info_key_cores')
                cores = Priority.variable(cores, self.info[info_key], info_key_cores)

                command = f'ElmerGrid 2 2 {mesh_name} -metis {cores} -force'
                run_command(command, case_path)
            case 'gMesh' | 'gmesh':

                case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
                
                mesh_name = options.get('mesh_name')
                info_key_mesh = options.get('info_key_mesh', 'e_mesh')
                mesh_name = Priority.variable(mesh_name, self.info[info_key], info_key_mesh)

                command1 = f'gmsh -3 {mesh_name}.geo'
                command2 = f'ElmerGrid 14 2 {mesh_name} -autoclean '

                run_command(command1, case_path)
                run_command(command2, case_path)
            case _:
                text = ''' You specifie incorrect argument what in run_decompose method.
                        The aviable list are 
                            * 'OF' or 'OpenFOAM' or 'openfoam' to run OpenFOAM decompose
                            * 'elmer' or 'Elemer' to run Elemer decompose. 
                        '''
                raise ValueError(text)

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

