import os
import sys
from Modules.AddtionalFunctions import change_var_fun


class Runner:
    """
        FIXME

    """
    def __init__(self, name='test', pathCase=None):
        self.name = name
        self.pyFoam = False
        self.mode = 'common'
        self.pathCase = pathCase

    def run_case(self, pathCase=None, decomposeOF=True, decomposeElmer=False):
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver
            NUMBER_OF_PROC_OF - is the number of processor cores involved to calculation of OpenFOAM problem
            NUMBER_OF_PROC_Elmer - is the number of processor cores involved to calculation of Elmer problem
            """

        path = self._priority_path(pathCase)
        os.chdir(path)

        if self.mode == 'common':
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py {self.solver_name}')
            else:
                os.system(f'{self.solver_name}')
        elif self.mode == 'parallel':
            self.decompose(decomposeOF)
            if self.pyFoam is True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.coreOF} {self.solver_name} -parallel :')
            else:
                os.system(f'mpirun -np {self.coreOF} {self.solver_name} -parallel :')
        elif self.mode == 'EOF':
            self.decompose(decomposeOF)
            self.decomposeElmer(decomposeElmer)
            if self.pyFoam is True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.coreOF} {self.solver_name} -parallel :')
            else:
                os.system(f'mpirun -np {self.coreOF} {self.solver_name} -parallel : '
                          f'-np {self.coreElmer} ElmerSolver_mpi | tee log -a')

    def decompose(self, decompose_OF: bool):
        os.chdir(self.pathCase)
        if decompose_OF is True:
            os.system('decomposePar -force')
        elif decompose_OF is False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def decomposeElmer(self, decompose_Elmer: bool):
        os.chdir(self.pathCase)
        if decompose_Elmer is True:
            os.system(f'ElmerGrid 2 2 {self.meshElmer} -metis {self.coreElmer} -force')
        elif decompose_Elmer is False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def set_PathCase(self, path_case):
        self.pathCase = path_case

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

    def set_decomposeParDict(self, coreOF=None, nameVar='core_OF', pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = os.path.join(self._priority_path(pathCase), 'system')
        coreOF = self._priority_cores(coreOF)
        os.chdir(path)
        print(os.getcwd())
        change_var_fun(nameVar, coreOF, nameFile='decomposeParDict')

    def setNameSolver(self, solver_name='pimpleFoam'):
        self.solver_name = solver_name
        print(f'You set name of solver as {self.solver_name}')

    def setModeRunner(self, mode='common'):
        self.mode = mode

    def setPyFoamSettings(self, pyFoam=False):
        self.pyFoam = pyFoam

    def set_fields(self, pathCase=None):
        path = self._priority_path(pathCase)
        os.chdir(path)
        os.system('setFields')

    def set_all_settings(self, dictionary):
        self.setPathCase(dictionary['newPath'])
        self.setCores(dictionary['numCoreOF'], dictionary['numCoreEOF'])
        self.setNameSolver(dictionary['solver_name'])
        self.setModeRunner(dictionary['mode'])
        self.setPyFoamSettings()

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
            if self.pathCase is not None:
                return self.pathCase
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
