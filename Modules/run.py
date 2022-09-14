import os
import sys
from Modules.auxiliary_functions import Priority, Files, Executer
from typing import Optional
from Modules.information import Information



class Run(Information):
    """
        FIXME

    """
    def __init__(self, info_key: Optional[str] = 'general',
                 solver: Optional[str] = 'pimpleFoam',
                 path_case: Optional[str] = None,
                 mode: Optional[str] = 'common'):
        Information.__init_runner__(self, info_key=info_key, case_path=path_case,
                                    solver=solver, mode=mode)
        self.info[info_key]['coreOF'] = 2  # number of cores to run openfoam
        self.info[info_key]['coreElmer'] = 2  # number of cores to run elmer
        self.info[info_key]['log'] = False  # flag to write log of solution procedure
        self.info[info_key]['pyFoam'] = False  # flag to run openfoam by pyFoam


    def __str__(self):
        #FIXME
        return f'It is myClass with var1 {self.info}'

    def __repr__(self):
        #FIXME
        return f'It is my collection of objects {self.info}'

    def run(self, path_case: Optional[str] = None, info_key=None) -> None:
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver

            """

        path_case = Priority.path(path_case, self.info[self.get_key(info_key)], path_key='case_path')
        Executer.run_command(self._collect_name_solver(info_key), path_case)

    def run_set_fields(self, path_case: str = None, info_key=None) -> None:
        run_path = self.get_path(info_key=info_key, case_path=path_case)
        command = 'setFields'
        Executer.run_command(command, run_path)

    def set_cores(self, coreOF: int = 4, coreElmer: int = 4, info_key=None) -> tuple:
        self.set_new_parameter(coreOF, parameter_name='coreOF', info_key=info_key)
        self.set_new_parameter(coreElmer, parameter_name='coreElmer', info_key=info_key)

    def set_cores_OF(self, coreOF: int = 4, info_key=None) -> int:
        self.set_new_parameter(coreOF, parameter_name='coreOF', info_key=info_key)

    def set_cores_Elmer(self, coreElmer: int = 4, info_key=None) -> int:
        self.set_new_parameter(coreElmer, parameter_name='coreElmer', info_key=info_key)

    def set_solver_name(self, solver_name: str ='pimpleFoam', info_key=None) -> None:
        self.set_new_parameter(solver_name, parameter_name='solver', info_key=info_key)

    def set_mode(self, mode: str = 'common', info_key=None) -> str:
        self.set_new_parameter(mode, parameter_name='mode', info_key=info_key)

    def set_pyFoam(self, pyFoam: bool = False, info_key=None) -> bool:
        self.set_new_parameter(pyFoam, parameter_name='pyFoam', info_key=info_key)

    def set_log_flag(self, log_flag: bool = False, info_key=None) -> bool:
        self.set_new_parameter(log_flag, parameter_name='log', info_key=info_key)




    def _collect_name_solver(self, info_key):
        """The function collect and crete required according setting name of solver

        """

        mode = self.get_any_parameter(parameter_name='mode', info_key=info_key)
        solver = self.get_any_parameter(parameter_name='solver', info_key=info_key)
        if mode == 'common':
            run_command = f'{solver}'
        elif mode == 'parallel':
            core_of = self.get_any_parameter(parameter_name='coreOF', info_key=info_key)
            run_command = f'mpirun -np {core_of} {solver} -parallel :'
        elif mode == 'EOF':
            core_of = self.get_any_parameter(parameter_name='coreOF', info_key=info_key)
            core_elmer = self.get_any_parameter(parameter_name='coreOF', info_key=info_key)
            run_command = f'mpirun -np {core_of} {solver} -parallel : ' \
                          f'-np {core_elmer} ElmerSolver_mpi'
        else:
            self._raise_error(True)

        if self.get_any_parameter(parameter_name='pyFoam') is True:
            run_command = 'pyFoamPlotRunner.py ' + run_command
        if self.get_any_parameter(parameter_name='log') is True:
            run_command += ' | tee log -a'

        self.set_new_parameter(run_command, parameter_name='run command', info_key=info_key)
        return self.get_any_parameter(parameter_name='run command')

    def _raise_error(self, status):
        if status is True:
            sys.exit('''you write not correct mode
                        Please chose from following modes:
                        common - general mode only for OpenFOAM;
                        parallel is the mode to run your case in parallel calculations
                        EOF is the mode to run your case with Elmer_old together''')