import os, sys
from Modules.AddtionalFunctions import changeVariablesFunV2


class Runner():

    def __init__(self, name='test', pathCase=None):
        self.name = name
        self.pyFoam = False
        self.mode = 'common'
        self.pathCase = pathCase


    def runCase(self, pathCase=None, decomposeOF=True, decomposeElmer=False):
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver
            NUMBER_OF_PROC_OF - is the number of processor cores involved to calculation of OpenFOAM problem
            NUMBER_OF_PROC_Elmer - is the number of processor cores involved to calculation of Elmer problem
            """

        path = self.priorityPath(pathCase)
        os.chdir(path)

        if self.mode == 'common':
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py {self.solverName}')
            else:
                os.system(f'{self.solverName}')
        elif self.mode == 'parallel':
            self.decompose(decomposeOF)
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.coreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.coreOF} {self.solverName} -parallel :')
        elif self.mode == 'EOF':
            self.decompose(decomposeOF)
            self.decomposeElmer(decomposeElmer)
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.coreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.coreOF} {self.solverName} -parallel : '
                          f'-np {self.coreElmer} ElmerSolver_mpi')


    def decompose(self, decomposeOF):
        if decomposeOF == True:
            os.system('decomposePar -force')
        elif decomposeOF == False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def decomposeElmer(self, decomposeElmer):
        if decomposeElmer == True:
            os.system(f'ElmerGrid 2 2 {self.meshElmer} -metis {self.coreElmer} -force')
        elif decomposeElmer == False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def setPathCase(self, pathCase):
        self.pathCase = pathCase

    def setCores(self, coreOF=4, CoreElmer=4):
        self.coreElmer = CoreElmer
        self.coreOF = coreOF

    def setCoresOF(self, coreOF=4):
        self.coreOF = coreOF

    def seCoresElmer(self, coreElmer=4, meshName=''):
        self.coreElmer = coreElmer
        self.meshElmer = meshName

    def setCoresEOF(self, coreOF=4, coreElmer=4, elmerMeshName=''):
        self.coreElmer = coreElmer
        self.meshElmer = elmerMeshName
        self.coreOF = coreOF

    def setDecomposeParDict(self, coreOF=None, nameVar='core_OF', pathCase=None):
        """The function serves to set *list of variables at controlDict for case with path of pathNewCase"""
        path = os.path.join(self.priorityPath(pathCase), 'system')
        coreOF = self.prioritCores(coreOF)
        os.chdir(path)
        print(os.getcwd())
        changeVariablesFunV2(nameVar, coreOF, nameFile='decomposeParDict')

    def setNameSolver(self, solverName='pimpleFoam'):
        self.solverName = solverName

    def setModeRunner(self, mode='common'):
        self.mode = mode

    def setPyFoamSettings(self, pyFoam=False):
        self.pyFoam = pyFoam

    def setFields(self, pathCase=None):
        path = self.priorityPath(pathCase)
        os.chdir(path)
        os.system('setFields')

    def setAllSettings(self, dictionary):
        self.setPathCase(dictionary['newPath'])
        self.setCores(dictionary['numCoreOF'], dictionary['numCoreEOF'])
        self.setNameSolver(dictionary['solverName'])
        self.setModeRunner(dictionary['mode'])
        self.setPyFoamSettings()







    def priorityPath(self, pathCase):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """

        if pathCase == None:
            if self.pathCase != None:
                return self.pathCase
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return pathCase

    def prioritCores(self, coreOF):
        if coreOF == None:
            if self.coreOF == None:
                sys.exit('You have to set numbers of cores for OpenFOAM')
            else:
                return self.coreOF
        else:
            return coreOF
