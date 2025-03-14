import os
import sys
import shutil
from distutils.dir_util import copy_tree
from ..additional_fun.auxiliary_functions import Priority, Files, run_command
from ..additional_fun.information import Information

class InitialValues(Information):
    """
    The class collects and process information dealing with initail values of
    models. 

    """

    def __init__(self, **optional_args):
        """

        Args:
            **optional_args:
                * info_key
                * case_path
                ...
        """
        Information.__init_iv__(self, **optional_args)

    def set_var(self, *zero_dicts: dict, **options):
        """The function sets given variables to sif file of Elemer
        Arguments:

            * *elmer_dicts is a set of dictionaries with keys as names or flags of variable in sif file
            * **options:
                * file_names = [],
                * case_path: Optional[str] = None,
                * info_key: Optional[str] = None

        Return: None

        """
        info_key = self.get_key(options.get('info_key'))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
        zero_path = self.get_any_folder_path('0', case_path, info_key=info_key)
        file_paths = Files.find_path_by_name(zero_path, file_names=options.get('file_names'))

        for file_path in file_paths:
            for zero_dict in zero_dicts:
                for var_name, value_var in zero_dict.items():
                    Files.change_var_fun(var_name, value_var, case_path, file_path)


    def reconstruct(self, case_path=None):
        "Запускает  ReconstrucPar"
        case_path = Priority.path(case_path, self.info, path_key='path')
        run_command('reconstructPar', case_path)

    def setTimeVaryingMappedFixedValue(self, case_path=None):
        "Устанавливает значения для ГУ TimeVaryingMappedFixedValue"
        zero_path = Priority.path(case_path, self.info, path_key='path') / '0'
        for var in self.dicTVMF:
            Files.change_var_fun(var, self.dicTVMF[var], path=zero_path, file_name='U')

    def settingsTimeVaryingMappedFixedValue(self, nameSample='outletSurf', sourceTimeStep=0.25, namePatch='outlet'):
        "Задает значения для ГУ TimeVaryingMappedFixedValue"
        dataDirpath = os.path.join(self.mappSettings['sPath'], 'postProcessing', nameSample)
        dataDir_var = os.path.relpath(dataDirpath, self.mappSettings['dPath'])
        points_var = f'{sourceTimeStep}/{namePatch}/points'
        sample_var = namePatch

        self.dicTVMF = {'dataDir_var': f'\"{dataDir_var}\"',
                        'points_var': f'\"{points_var}\"',
                        'sample_var': f'{sample_var}'}
        self.checkPathTVMF = dataDirpath

    
    def set_mapping_settings(self, src_path, dst_path, src_time=0, dst_time=0):
        self.mapp_settings = dict(src_path=Priority.path(src_path, None),
                                    dst_path=Priority.path(dst_path, None),
                                    src_time=str(src_time),
                                    dst_time=str(dst_time)
                                  )

    def set_map_values(self, src_path=None, dst_path=None, src_time=0, dst_time=0):
        """
        копирует содержимое src_time из src_path/ в dst_path с новым именем dst_time
        """
        src_path = Priority.path(src_path, self.mapp_settings, path_key='src_path')
        dst_path = Priority.path(dst_path, self.mapp_settings, path_key='dst_path')
        Files.copy_file(src_path, dst_path, old_name=src_time, new_name=dst_time)
    
    def run_mapFields(self, **options):
        """
        The method run mapFields utilit 

        Argments:
        * **options:
            * case_path: Optional[str] = None,
            * info_key: Optional[str] = None
            * check: Optional[Bool] = False

        """
        info_key = self.get_key(options.get('info_key', None))
        case_path = Priority.path(options.get('case_path'), self.info[info_key], path_key='case_path')
        check_status = options.get('check', False)
       
        if check_status:
            self.__checkFileForMapFields()
            run_command(self.commandMapFields, case_path)
        else:
            run_command(self.commandMapFields, case_path)

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
                       '-noFunctionObjects': noFunctionObjects,
                       '-mapMethod': mapMethod,
                       '-parallelSource': parallelSource,
                       '-parallelTarget': parallelTarget,
                       '-sourceTime': sourceTime,
                       'src': relpath_src}

        return self.option

    def createMapFieldCommand(self, option=None):
        command = 'mapFields'
        option = self.__checkOption(option)

        for key in option:
            if option[key] is True:
                command += f' {key}'
            elif option[key] is False:
                pass
            elif key == 'src':
                command += f' {option[key]}'
            elif key == '-sourceTime':
                if option[key] == 'latestTime':
                    command += f' {key} \'latestTime\''
                else:
                    command += f' {key} {option[key]}'
            else:
                command += f' {key} {option[key]}'
        self.commandMapFields = command
        return command

    def copyBC(self, nameBCsource='outlet', nameBCdist='inlet', mapTimeStep=0.25, namePostFile='outletSurf'):
        """Эта функция копирует значения из postProcessing в заданном времени (mapTimeStep)
        в кейс назначения в папку constant """

        pathScalar = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource, 'scalarField')
        pathVector = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource, 'vectorField')
        pathPoints = os.path.join(self.mappSettings['sPath'], 'postProcessing', namePostFile,
                                  str(mapTimeStep), nameBCsource, 'points')

        pathBCdist = os.path.join(self.mappSettings['dPath'], 'constant', 'boundaryData', nameBCdist)

        if os.path.exists(pathScalar):
            copy_tree(pathScalar, os.path.join(pathBCdist, '0'))
        copy_tree(pathVector, os.path.join(pathBCdist, '0'))
        shutil.copy(pathPoints, pathBCdist)

    def run_set_fields(self, path_case: str = None, info_key=None) -> None:
        run_path = self.get_path(info_key=info_key, case_path=path_case)
        command = 'setFields'
        run_command(command, run_path)

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
    def calcInitVal_cylindr(self, Dh, Uin, nu):
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
        e is predict disspation rate
        Dh is hydrolic diametr"""

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


    def __checkOption(self, option):
        if option == None:
            if self.option != None:
                return self.option
            else:
                sys.exit('You need to write option of mapFields')
        else:
            return option

    def __checkFileForMapFields(self):
        testPath = os.path.join(self.checkPathTVMF, '0')
        if not os.path.exists(testPath):
            Files.copy_file(self.checkPathTVMF, self.checkPathTVMF, '0', '0.25')
            return True
        else:
            print('The 0 file is exist')
            return True
