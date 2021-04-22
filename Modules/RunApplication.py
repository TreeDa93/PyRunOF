import os, sys

class Runner():

    def __init__(self, name='test', pathCase=None):
        self.name = name
        self.pyFoam = False
        self.mode = 'common'
        self.pathCase = pathCase

    def setFields(self, pathCase=None):
        path = self.priorityPath(pathCase)
        os.chdir(path)
        os.system('setFields')

    def runCase(self, pathCase=None, decompose=True):
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
            self.decompose(decompose)
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
        elif self.mode == 'EOF':
            self.decompose(decompose)
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.numCoreOF} {self.solverName} -parallel : '
                          f'-np {self.numCoreElmer} ElmerSolver_mpi')


    def decompose(self, decompose):
        if decompose == True:
            os.system('decomposePar -force')
        elif decompose == False:
            print('Decompose procedure is pass')
        else:
            sys.exit('The decompose status is no bolean')

    def setPathCase(self, pathCase):
        self.pathCase = pathCase

    def setCores(self, numCoreOF=4, numCoreElmer=4):
        self.numCoreOF = numCoreOF
        self.numCoreElmer = numCoreElmer

    def setNameSolver(self, solverName='pimpleFoam'):
        self.solverName = solverName

    def setModeRunner(self, mode='common'):
        self.mode = mode

    def setPyFoamSettings(self, pyFoam=False):
        self.pyFoam = pyFoam

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
