import os

class Runner():

    def __init__(self, name='test'):
        self.name = name
        self.pyFoam = False
        self.mode = 'common'


    def runCase(self):
        """The function runs the case to calculation
            Variables:
            Name_solver is the name of the OpenFOAM solver
            NUMBER_OF_PROC_OF - is the number of processor cores involved to calculation of OpenFOAM problem
            NUMBER_OF_PROC_Elmer - is the number of processor cores involved to calculation of Elmer problem
            """

        os.chdir(self.newPath)
        if self.mode == 'common':
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py {self.solverName}')
            else:
                os.system(f'{self.solverName}')
        elif self.mode == 'parallel':
            os.system('decomposePar -force')
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
        elif self.mode == 'EOF':
            os.system('decomposePar -force')
            if self.pyFoam == True:
                os.system(f'pyFoamPlotRunner.py mpirun -np {self.numCoreOF} {self.solverName} -parallel :')
            else:
                os.system(f'mpirun -np {self.numCoreOF} {self.solverName} -parallel : '
                          f'-np {self.numcoreEOF} ElmerSolver_mpi')


    def setNewPathCase(self, newPath):
        self.newPath = newPath

    def setCores(self, numCoreOF=4, numCoreEOF=4):
        self.numCoreOF = numCoreOF
        self.numcoreEOF = numCoreEOF

    def setNameSolver(self, solverName='pimpleFoam'):
        self.solverName = solverName

    def setModeRunner(self, mode='common'):
        self.mode = mode

    def setPyFoamSettings(self, pyFoam=False):
        self.pyFoam = pyFoam

    def setAllSettings(self, dictionary):
        self.setNewPathCase(dictionary['newPath'])
        self.setCores(dictionary['numCoreOF'], dictionary['numCoreEOF'])
        self.setNameSolver(dictionary['solverName'])
        self.setModeRunner(dictionary['mode'])
        self.setPyFoamSettings()


