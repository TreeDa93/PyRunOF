import os
import sys
import shutil
import datetime


class Manipulations:
    """
    FIXME

    """
    def __init__(self, name='firts', runPath=None, newPath=None, basePath=None):
        self.name = name
        self.pathes = {'newPath': newPath,
                       'basePath': basePath,
                        'runPath' : runPath}
        self.namesCases = {'newName': None}

    def __repr__(self):
        return f"Name of manipulation node ({self.name}, runpath {self.pathes['runPath']}, basepath " \
               f"{self.pathes['basePath']}, newPath {self.pathes['newPath']})"

    def __str__(self):
        return f"Name of manipulation node ({self.name}, runpath {self.pathes['runPath']}, basepath " \
               f"{self.pathes['basePath']}, newPath {self.pathes['newPath']})"

    def dublicateCase(self, basePath=None, newPath=None, keyPathes=('basePath', 'newPath'),
                      keyNames=('baseName', 'newName'), mode='copy'):
        """The function creates copy of the base case.
           pathBaseCase is the path of base case that will be copied by the function
           pathNewCase is the path of new case that will be created by the function
           mode defines how the procedure of copying will be done.
                   a) rewrite mode is the mode when folder of new case already being existed, then the folder
                   will delited by the function and base case folder will be copied to the folder being the same name
                   b) copy mode is the mode when folder of new case already being existed, then the folder will be copied
                   to the folder being old name with prefix of current time of copying. And new case will be copied
                    to folder being path of pathNewCase variables."""


        basePath, newPath = self.priorityPath(basePath, newPath)

        self.checkExistence(basePath, newPath)

        if mode == 'rewrite':
                print(f'The folder {os.path.basename(newPath)}  is exist. The script run the rewrite mode')
                shutil.rmtree(newPath)
                shutil.copytree(basePath, newPath)
        elif mode == 'copy':
                print(f'The folder {os.path.basename(newPath)}  is exist. The script run the copy mode')
                now = datetime.datetime.now()
                old_file = newPath + '_' + 'old' + '_' + now.strftime("%d-%m-%Y %H:%M")
                try:
                    shutil.move(newPath, old_file)
                    self.oldNameCase = os.path.basename(old_file)
                except shutil.Error:
                    print('You run the script is often. There is exception old case')
                shutil.copytree(basePath, newPath)
        else:
                shutil.copytree(basePath, newPath)
        self.pathes[keyPathes[0]] = basePath
        self.pathes[keyPathes[1]] = newPath
        self.namesCases[keyNames[0]] = os.path.basename(basePath)
        self.namesCases[keyPathes[1]] = os.path.basename(newPath)

    def generatorNewName(self, *namesNewCase, baseNewName='', keyName='newName', splitter='_'):
        """The function serves to create two variables of base and new case paths.
        The name of new case is generated by special algorithm realized in the fucntion.
        The name will be created by adding variables of the list namesNewCase to base case folder name. The variables
        will be seprated by special sympol (spliter) to name of the folder.
         Variables:
                    *namesNewCase is a number of variables, which will be added to name of new case
                    baseCase is the folder name of base case
                    splitter is the variables defending the for separation in folder name of new case """
        for addName in namesNewCase:
            baseNewName += splitter + str(addName)

        self.namesCases[keyName] = baseNewName
        return self.namesCases[keyName]

    def createNewPath(self, dirmame=None, newCaseName=None, keyPath='newPath'):
        """The function is used for creating new path
        Variables
        dirname is the path of directory where new folder of case put
        newCaseName is the name of new case

        newPath is the path of new case
        """
        self.pathes[keyPath] = os.path.join(dirmame, newCaseName)
        return self.pathes[keyPath]


    def changePath(self, path, keyPath='newPath'):
        """The function is used for changing existent path by name
        Input variables
        path is new given path
        key is the name of variables of key for dictionary of addtionals pathes"""
        if keyPath in self.pathes.keys():
            self.pathes[keyPath] = path
        else:
            print('Error the key of path is not exist!')


    def createYourPath(self, path, keyPath='testPath'):
        """The function is used to create your own path
        The created path will be written into dictionary self.addtionaldictionary with key  = name
        Input path is path of your new given path
        name is the key of dictionary storaged all addtional pathes"""
        self.pathes[keyPath] = path


    def getPath(self, keyPath):
        """The methods gives back path acording givven name or key
        Input:
        key is the name of class variables consisting pathes or key of dictionary with pathes """
        if keyPath in self.pathes.keys():
            return self.pathes[keyPath]
        else:
            print('Error: The given name of key with pathes is not exist!')

    def getName(self, keyName):
        """The methods gives back path acording givven name or key
        Input:
        key is the name of class variables consisting pathes or key of dictionary with pathes """
        if keyName in self.namesCases.keys():
            return self.namesCases[keyName]
        else:
            print('Error: The given name of key with pathes is not exist!')


    def checkExistence(self, basePath, newPath):
        """The method supports to find out existing gotten pathes
        If one of the gotten pathes is not exist, program is interupted
        """

        if not os.path.exists(basePath):
            sys.exit('Error: The base case is not exist in the directory!!!')
        elif not os.path.exists(newPath):
            dirname, newCaseName = os.path.split(newPath)
            if os.path.exists(dirname):
                os.mkdir(f'{newPath}')
            else:
                sys.exit(f'Error: The new path {dirname} is not exist !!!')


    def priorityPath(self, basePath, newPath):
        """The method is used for selection of given path
        the first priority is given path by methods
        the second priority is given path by class constructor
        If both path is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """

        if basePath == None:
            if self.pathes['basePath'] != None:
                retrunBasePath = self.pathes['basePath']
            else:
                sys.exit('Error: You do not enter the base path!!!')
        else:
            retrunBasePath = basePath

        if newPath == None:
            if self.pathes['newPath'] != None:
                returnNewPath = self.pathes['newPath']
            else:
                sys.exit('Error: You do not enter the new path!!!')
        else:
            returnNewPath = newPath

        return retrunBasePath, returnNewPath