import os, sys, shutil, datetime



class Manipulations():

    def __init__(self):
        test = 1



    def dublicateCase(self, baseCasePath='', newPath='', mode=''):
        """The function creates copy of the base case.
           pathBaseCase is the path of base case that will be copied by the function
           pathNewCase is the path of new case that will be created by the function
           mode defines how the procedure of copying will be done.
                   a) rewrite mode is the mode when folder of new case already being existed, then the folder
                   will delited by the function and base case folder will be copied to the folder being the same name
                   b) copy mode is the mode when folder of new case already being existed, then the folder will be copied
                   to the folder being old name with prefix of current time of copying. And new case will be copied
                    to folder being path of pathNewCase variables."""

        self.checkExistence(baseCasePath, newPath)

        if mode == 'rewrite':
                print(f'The folder {os.path.basename(newPath)}  is exist. The script run the rewrite mode')
                shutil.rmtree(newPath)
                shutil.copytree(baseCasePath, newPath)
        elif mode == 'copy':
                print(f'The folder {os.path.basename(newPath)}  is exist. The script run the copy mode')
                now = datetime.datetime.now()
                old_file = newPath + '_' + 'old' + '_' + now.strftime("%d-%m-%Y %H:%M")
                try:
                    shutil.move(newPath, old_file)
                except shutil.Error:
                    print('You run the script is often. There is exception old case')
                shutil.copytree(baseCasePath, newPath)
        else:
                shutil.copytree(baseCasePath, newPath)


    def checkExistence(self, baseCasePath, newPath):
        if not os.path.exists(baseCasePath):
            sys.exit('Error: The base case is not exist in the directory!!!')
        elif not os.path.exists(newPath):
            dirname, newFolder = os.path.split(newPath)
            if os.path.exists(dirname):
                os.mkdir(f'{newFolder}')
            else:
                sys.exit(f'Error: The new path {dirname} is not exist !!!')
