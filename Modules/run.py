import os
import sys
from Modules.auxiliary_functions import change_var_fun


class Run:
    """
        FIXME

    """
    def __init__(self, name='test', path_case=None):
        self.name = name
        self.pyFoam = False
        self.logFlag = False
        self.mode = 'common'
        self.path_case = path_case

    def __str__(self):
        return f'It is myClass with var1 {self.name}'

    def __repr__(self):
        return f'It is my collection of objects {self.name}'

    def run(self, path_case=None, decompose_OF=True, decompose_Elmer=False) -> None:
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver
            NUMBER_OF_PROC_OF - is the number of processor cores involved to calculation of OpenFOAM problem
            NUMBER_OF_PROC_Elmer - is the number of processor cores involved to calculation of Elmer problem
            """

        path = self._priority_path(path_case)
        os.chdir(path)
        self.decompose_run(self, decompose_OF, decompose_Elmer)
        os.system(self._collect_name_solver())

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
            os.system(f'ElmerGrid 2 2 {self.meshElmer} -metis {self.coreElmer} -force')
        elif decompose_Elmer is False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def set_path_case(self, path_case):
        self.path_case = path_case

    def set_cores(self, coreOF=4, coreElmer=4):
        self.coreOF = coreOF
        self.coreElmer = coreElmer

    def set_cores_OF(self, coreOF=4):
        self.coreOF = coreOF

    def set_cores_Elmer(self, coreElmer=4, meshName=''):
        self.coreElmer = coreElmer
        self.meshElmer = meshName

    def set_cores_EOF(self, coreOF=4, coreElmer=4, elmerMeshName=''):
        self.coreElmer = coreElmer
        self.meshElmer = elmerMeshName
        self.coreOF = coreOF

    def set_decomposeParDict(self, core_OF=None, name_var='core_OF', path_case=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = os.path.join(self._priority_path(path_case), 'system')
        core_OF = self._priority_cores(core_OF)
        os.chdir(path)
        print(os.getcwd())
        change_var_fun(name_var, core_OF, nameFile='decomposeParDict')

    def set_solver_name(self, solver_name='pimpleFoam'):
        self.solver_name = solver_name
        print(f'You set name of solver as {self.solver_name}')

    def set_mode(self, mode='common'):
        self.mode = mode

    def set_pyFoam_settings(self, pyFoam=False):
        self.pyFoam = pyFoam

    def set_log_flag(self, log_flag=False):
        self.logFlag = log_flag

    def set_fields(self, path_case=None):
        path = self._priority_path(path_case)
        os.chdir(path)
        os.system('setFields')

    def set_all_settings(self, dictionary):
        self.set_path_case(dictionary['newPath'])
        self.set_cores(dictionary['numCoreOF'], dictionary['numCoreEOF'])
        self.set_solver_name(dictionary['solver_name'])
        self.set_mode(dictionary['mode'])
        self.set_pyFoam_settings()
        self.set_log_flag()

    def decompose_run(self, decompose_OF: int, decompose_Elmer: int):
        if self.mode == 'common':
            if decompose_OF is True:
                print('You do not need to run decompasition for common mode')
        elif self.mode == 'parallel':
            self.decompose_OF(decompose_OF)
        elif self.mode == 'EOF':
            self.decompose_OF(decompose_OF)
            self.decompose_Elmer(decompose_Elmer)

    def _collect_name_solver(self):
        """The function collect and crete required according setting name of solver

        """

        if self.mode == 'common':
            run_command = f'{self.solver_name}'
        elif self.mode == 'parallel':
            run_command = f'mpirun -np {self.self.coreOF} {self.solver_name} -parallel :'
        elif self.mode == 'EOF':
            run_command = f'mpirun -np {self.self.coreOF} {self.solver_name} -parallel : ' \
                          f'-np {self.coreElmer} ElmerSolver_mpi'
        else:
            sys.exit('''you write not correct mode
             Please chose from following modes:
             common - general mode only for OpenFOAM;
             parallel is the mode to run your case in parallel calculations
             EOF is the mode to run your case with Elmer together''')

        if self.pyFoam is True:
            run_command = 'pyFoamPlotRunner.py ' + run_command
        if self.logFlag is True:
            run_command += ' | tee log -a'

        self.run_command = run_command
        return self.run_command

    def _priority_path(self, path_case):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """

        if path_case is None:
            if self.path_case is not None:
                return self.path_case
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return path_case

    def _priority_cores(self, core_OF):
        if core_OF is None:
            if self.core_OF is not None:
                return self.core_OF
            else:
                sys.exit('You have to set numbers of cores for OpenFOAM')
        else:
            return core_OF
