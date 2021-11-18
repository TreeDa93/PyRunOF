import os
import sys
import shutil
from distutils.dir_util import copy_tree
from Modules.auxiliary_functions import change_var_fun, copy_fun


class InitialValue:
    """
    FIXME

    """

    def __init__(self, pathCase=None,  dictionary=None):
        self.pathCase = pathCase
        if pathCase == None:
            self.path = None
        else:
            self.path = os.path.join(pathCase, '0')
        self.dictionary = dictionary

    def setVarAllFiles(self, *varDict, pathCase=None):

        dictionary = self.priorityDictionary(varDict)
        path = self.priorityPath(pathCase)
        fileList = os.listdir(self.path)
        os.chdir(path)
        for file in fileList:
            for list in dictionary:
                for var in list:
                    change_var_fun(var, list[var], nameFile=file)

    def setVar(self, *varDict, nameFiels=['U', 'k'], pathCase=None):
        """Устанавливает значение перенных из словарей *varDict в файлах из списка nameFiels
        в кейсе path_case"""
        dictionary = self.priorityDictionary(varDict)
        path = self.priorityPath(pathCase)

        os.chdir(path)
        for file in nameFiels:
            for list in dictionary:
                for var in list:
                    change_var_fun(var, list[var], nameFile=file)

    def setMappSettings(self, sourcePath=None, distPath=None, source='0.25', dist='0'):
        self.mappSettings = {}
        self.mappSettings['sPath'] = os.path.abspath(sourcePath)
        self.mappSettings['dPath'] = os.path.abspath(distPath)
        self.mappSettings['source'] = source
        self.mappSettings['dist'] = dist

    def setMappValues(self):
        "Копирует папку source в dist из пути source в  dist"
        sourcePath = os.path.join(self.mappSettings['sPath'], self.mappSettings['source'])
        distPath = os.path.join(self.mappSettings['dPath'], self.mappSettings['dist'])
        copy_fun(sourcePath, distPath)

    def reconstruct(self, pathCase):
        "Запускает  ReconstrucPar"
        os.chdir(pathCase)
        os.system('reconstructPar')

    def setTimeVaryingMappedFixedValue(self, pathCase=None):
        "Устанавливает значения для ГУ TimeVaryingMappedFixedValue"
        path = self.priorityPath(pathCase)
        os.chdir(path)

        for var in self.dicTVMF:
            change_var_fun(var, self.dicTVMF[var], nameFile='U')

    def settingsTimeVaryingMappedFixedValue(self, nameSample='outletSurf', sourceTimeStep = 0.25, namePatch = 'outlet'):
        "Задает значения для ГУ TimeVaryingMappedFixedValue"
        dataDirpath = os.path.join(self.mappSettings['sPath'], 'postProcessing', nameSample)
        dataDir_var = os.path.relpath(dataDirpath, self.mappSettings['dPath'])
        points_var = f'{sourceTimeStep}/{namePatch}/points'
        sample_var = namePatch

        self.dicTVMF = {'dataDir_var': f'\"{dataDir_var}\"',
                      'points_var': f'\"{points_var}\"',
                      'sample_var': f'{sample_var}'}
        self.checkPathTVMF = dataDirpath


    def mapFieldsRun(self, pathCase=None, check=False):

        path = self.priorityPathCase(pathCase)
        os.chdir(path)
        print(path)
        if check:
            self.checkFileForMapFields()
            os.system(self.commandMapFields)
        else:
            os.system(self.commandMapFields)


    def settingsMapField(self, sourcePath=None, distPath=None, consistent=True,
                         mapMethod='mapNearest', parallelSource=True,
                         parallelTarget=False, sourceTime=0.25, noFunctionObjects=True):
        """ Usage: mapFields [OPTIONS] <sourceCase>
          options:
            -case <dir>       specify alternate case directory, default is the cwd
            -consistent       source and target geometry and boundary conditions identical
            -fileHandler <handler>
                              override the fileHandler
            -mapMethod <word>
                              specify the mapping method
                              'mapNearest, interpolate, cellPointInterpolate'
            -noFunctionObjects
                              do not execute functionObjects
            -parallelSource   the source is decomposed
            -parallelTarget   the target is decomposed
            -sourceRegion <word>
                              specify the source region
            -sourceTime <scalar|'latestTime'>
                              specify the source time
            -subtract         subtract mapped source from target
            -targetRegion <word>
                              specify the target region
            -srcDoc           display source code in browser
            -doc              display application documentation in browser
            -help             print the usage
          """


        if sourcePath == None:
            path_src = self.mappSettings['sPath']
        else:
            path_src = sourcePath

        if distPath == None:
            path_dst = self.mappSettings['dPath']
        else:
            path_dst = distPath

        relpath_src = os.path.relpath(path_src, path_dst)
        relpath_dst = os.path.relpath(path_dst, path_dst)


        self.option = {'-case': relpath_dst,
                  '-consistent': consistent,
                  '-noFunctionObjects' : noFunctionObjects,
                  '-mapMethod': mapMethod,
                  '-parallelSource': parallelSource,
                  '-parallelTarget': parallelTarget,
                  '-sourceTime': sourceTime,
                  'src': relpath_src}

        return self.option

    def createMapFieldCommand(self, option=None):
        command = 'mapFields'
        option = self.checkOption(option)

        for key in option:
            if option[key] is True:
                command+= f' {key}'
            elif option[key] is False:
                pass
            elif key == 'src':
                command+= f' {option[key]}'
            elif key == '-sourceTime':
                if option[key] == 'latestTime':
                    command += f' {key} \'latestTime\''
                else:
                    command += f' {key} {option[key]}'
            else:
                command+= f' {key} {option[key]}'
        self.commandMapFields = command
        print(self.commandMapFields)
        return command


    def copyBC(self, nameBCsource='outlet', nameBCdist='inlet', mapTimeStep=0.25, namePostFile='outletSurf'):
        """Эта функция копирует значения из postProcessing в заданном времени (mapTimeStep)
        в кейс назначения в папку constant """

        pathScalar = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource,'scalarField')
        pathVector = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource,'vectorField')
        pathPoints = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource, 'points')

        pathBCdist = os.path.join(self.mappSettings['dPath'], 'constant', 'boundaryData', nameBCdist)

        if os.path.exists(pathScalar):
            copy_tree(pathScalar, os.path.join(pathBCdist, '0'))
        copy_tree(pathVector, os.path.join(pathBCdist, '0'))
        shutil.copy(pathPoints, pathBCdist)

    def calcInitVal(self, A, B, Uin, nu):
        """The function serves to calculate intial values required for improving convergence of task. The function
        gives dictionaries with key of variables and them values. Keys of variables is chosen as way as in fiels of OF.
        Input variables:
        Uin is the inlet velocity
        nu is the kinematic viscosity
        Output variables
        Dh is hydrolic diametr
        Re is the Reynolds number
        I is the intensivity of flow
        L is mixing length scale
        k is predict kinetic energy
        omega is predict specific dissipation rate
        e is predict disspation rate"""
        Dh = 4 * A * B / (2 * (A + B))  # hydrolic diametr
        Re = Uin * Dh / nu  # Reynolds number
        I = 0.16 * Re ** (-0.125)  # Intensity
        L = Dh * I  # mix length    scale
        k = 1.5 * (I * Uin) ** 2  # kinetic energy
        omega = k ** 0.5 / (0.09 ** 0.25 * L)  # specific dissipation rate
        e = 0.09 ** 0.75 * k ** 1.5 / L  # dissipation rate
        dict = {'Dh_var': Dh,
                'Re_var': Re,
                'Ical_var': I,
                'L_var': L,
                'k_var': k,
                'omega_var': omega,
                'ep_var': e,
                }
        return dict



    def priorityDictionary(self, varDict):
        if varDict==None:
            if self.dictionary != None:
                return self.dictionary
            else:
                sys.exit('ERROR: The dictonary is not exist')
        else:
            return varDict

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
                return self.path
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            return os.path.join(pathCase, '0')


    def priorityPathCase(self, pathCase):
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
            return os.path.join(pathCase)




    def checkOption(self, option):
        if option == None:
            if self.option != None:
                return self.option
            else:
                sys.exit('You need to write option of mapFields')
        else:
            return option

    def checkFileForMapFields(self):
        os.chdir(self.pathCase)
        testPath = os.path.join(self.checkPathTVMF, '0')
        if not os.path.exists(testPath):
            copypath = os.path.join(self.checkPathTVMF, '0.25')
            copy_fun(copypath, testPath)
            return True
        else:
            print('The 0 file is exist')
            return True