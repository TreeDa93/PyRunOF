import sys
from typing import Optional
from ..additional_fun.auxiliary_functions import Priority, run_command
from ..additional_fun.information import Information


class Run(Information):
    """
        #FIXME

    """
    def __init__(self, **optional_args):
        """
        Args:
            **optional_args:
                * info_key: Optional[str] = 'general',
                * solver: Optional[str] = 'pimpleFoam',
                * path_case: Optional[str] = None,
                * mode: Optional[str] = 'common'
        """
        Information.__init_runner__(self, **optional_args)


    def __str__(self):
        #FIXME
        return f'It is myClass with var1 {self.info}'

    def __repr__(self):
        #FIXME
        return f'It is my collection of objects {self.info}'

    def run(self, **options) -> None:
        """The function runs the case to calculation
            Arguments:
            
            * **options is the optional arguments listed below: 

                * case_path: Optional[str] = None,
                * info_key=None

            """

        info_key = self.get_key(options.get('info_key'))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
        run_command(self._collect_name_solver(info_key), case_path)

    def run_set_fields(self, path_case: str = None, info_key=None) -> None:
        run_path = self.get_path(info_key=info_key, case_path=path_case)
        command = 'setFields'
        run_command(command, run_path)

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

        mode = self.get_any_parameter('mode', info_key=info_key)
        solver = self.get_any_parameter('solver', info_key=info_key)
        if mode == 'common':
            run_command = f'{solver}'
        elif mode == 'parallel':
            core_of = self.get_any_parameter('coreOF', info_key=info_key)
            run_command = f'mpirun -np {core_of} {solver} -parallel :'
        elif mode == 'EOF':
            core_of = self.get_any_parameter('coreOF', info_key=info_key)
            core_elmer = self.get_any_parameter('coreOF', info_key=info_key)
            run_command = f'mpirun -np {core_of} {solver} -parallel : ' \
                          f'-np {core_elmer} ElmerSolver_mpi'
        else:
            self._raise_error(True)

        if self.get_any_parameter('pyFoam') is True:
            run_command = 'pyFoamPlotRunner.py ' + run_command
        if self.get_any_parameter('log') is True:
            run_command += ' | tee log -a'

        self.set_new_parameter(run_command, parameter_name='run command', info_key=info_key)
        return self.get_any_parameter('run command')

    def _raise_error(self, status):
        if status is True:
            sys.exit('''you write not correct mode
                        Please chose from following modes:
                        common - general mode only for OpenFOAM;
                        parallel is the mode to run your case in parallel calculations
                        EOF is the mode to run your case with Elmer_old together''')