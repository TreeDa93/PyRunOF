import os
import sys
from Modules.auxiliary_functions import Priority, Files
from typing import List, Optional, Dict


class Run:
    """
        FIXME

    """
    def __init__(self, name='test',
                 path_case: Optional[str] = None,
                 solver_name: Optional[str] = 'pimpleFoam',
                 mode: Optional[str] = 'common',
                 coreOF: Optional[int] = 4,
                 coreElmer: Optional[int] = 4,
                 mesh_Elmer: Optional[str] = '',
                 pyFoam: Optional[bool] = False,
                 log_lag: Optional[bool] = False):

        self.name = name
        self.path_case = path_case
        self.solver_name = solver_name
        self.pyFoam = pyFoam
        self.log_flag = log_lag
        self.mode = mode
        self.coreOF = coreOF
        self.coreElmer = coreElmer
        self.mesh_Elmer = mesh_Elmer

    def __str__(self):
        return f'It is myClass with var1 {self.name}'

    def __repr__(self):
        return f'It is my collection of objects {self.name}'

    def run(self, path_case: Optional[str] = None,
            path_key: Optional[str] = None,
            decompose_OF: Optional[bool] = True,
            decompose_Elmer: Optional[bool] = False) -> None:
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver
            NUMBER_OF_PROC_OF - is the number of processor cores involved to calculation of OpenFOAM problem
            NUMBER_OF_PROC_Elmer - is the number of processor cores involved to calculation of Elmer problem
            """
        run_path = Priority.path(path_case, path_key, self.path_case)
        os.chdir(run_path)
        self.decompose_run(decompose_OF, decompose_Elmer)
        os.system(self._collect_name_solver())

    def decompose_run(self, decompose_OF: bool, decompose_Elmer: bool):
        if self.mode == 'common':
            if decompose_OF is True:
                print('You do not need to run decompasition for common mode')
        elif self.mode == 'parallel':
            self.decompose_OF(decompose_OF)
        elif self.mode == 'EOF':
            self.decompose_OF(decompose_OF)
            self.decompose_Elmer(decompose_Elmer)

    def decompose_OF(self, decompose_OF: bool) -> None:
        os.chdir(self.path_case)
        if decompose_OF is True:
            os.system('decomposePar -force')
        elif decompose_OF is False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no boolean')

    def decompose_Elmer(self, decompose_Elmer: bool):
        os.chdir(self.path_case)
        if decompose_Elmer is True:
            os.system(f'ElmerGrid 2 2 {self.mesh_Elmer} -metis {self.coreElmer} -force')
        elif decompose_Elmer is False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def set_path_case(self, path_case: str) -> str:
        self.path_case = path_case
        return self.path_case

    def set_cores(self, coreOF: int = 4, coreElmer: int = 4) -> tuple:
        self.coreOF = coreOF
        self.coreElmer = coreElmer
        return self.coreOF, self.coreElmer

    def set_cores_OF(self, coreOF: int = 4) -> int:
        self.coreOF = coreOF
        return self.coreOF

    def set_cores_Elmer(self, coreElmer: int = 4) -> int:
        self.coreElmer = coreElmer
        return self.coreElmer

    def set_Elmer_mesh_name(self, mesh_name: str) -> str:
        self.mesh_Elmer = mesh_name
        return self.mesh_Elmer

    def set_decomposeParDict(self,
                             core_OF: int = None,
                             name_var: str = 'core_OF',
                             path_case: str = None):
        """The function serves to set *list of variables at controlDict for case with name of pathNewCase"""
        path_case = Priority.variable(path_case, '', self.path_case)
        sys_path = os.path.join(path_case, 'system')
        core_OF = Priority.cores(core_OF, self.coreOF)
        Files.change_var_fun(name_var, core_OF, path=sys_path, file_name='decomposeParDict')

    def set_solver_name(self, solver_name: str ='pimpleFoam') -> None:
        self.solver_name = solver_name
        print(f'You set name of solver as {self.solver_name}')

    def set_mode(self, mode: str = 'common') -> str:
        self.mode = mode
        return self.mode

    def set_pyFoam_settings(self, pyFoam: bool = False) -> bool:
        self.pyFoam = pyFoam
        return self.pyFoam

    def set_log_flag(self, log_flag: bool = False) -> bool:
        self.log_flag = log_flag
        return bool

    def set_fields(self, path_case: str = None) -> None:
        run_path = Priority.variable(path_case, '', self.path_case)
        os.chdir(run_path)
        os.system('setFields')

    def set_all_settings(self, dic_settings: dict):
        """
        Dict['runPath': str,
                    'coreOF': int, 'coreElmer': int, 'solver': str,
                    'mode' : str,
                    'ElmerMesh': str, 'pyFoam': bool, 'log': bool
                    ]
        """
        self.set_path_case(dic_settings.get('runPath'))
        self.set_cores(dic_settings.get('coreOF'), dic_settings.get('coreElmer'))
        self.set_solver_name(dic_settings.get('solver'))
        self.set_mode(dic_settings.get('mode'))
        self.set_Elmer_mesh_name(dic_settings.get('ElmerMesh'))
        self.set_pyFoam_settings(dic_settings.get('pyFoam'))
        self.set_log_flag(dic_settings.get('log'))

    def _collect_name_solver(self):
        """The function collect and crete required according setting name of solver

        """

        if self.mode == 'common':
            run_command = f'{self.solver_name}'
        elif self.mode == 'parallel':
            run_command = f'mpirun -np {self.coreOF} {self.solver_name} -parallel :'
        elif self.mode == 'EOF':
            run_command = f'mpirun -np {self.coreOF} {self.solver_name} -parallel : ' \
                          f'-np {self.coreElmer} ElmerSolver_mpi'
        else:
            sys.exit('''you write not correct mode
             Please chose from following modes:
             common - general mode only for OpenFOAM;
             parallel is the mode to run your case in parallel calculations
             EOF is the mode to run your case with Elmer together''')

        if self.pyFoam is True:
            run_command = 'pyFoamPlotRunner.py ' + run_command
        if self.log_flag is True:
            run_command += ' | tee log -a'

        self.run_command = run_command
        return self.run_command