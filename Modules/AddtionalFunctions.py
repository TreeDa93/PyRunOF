import os

def changeVariablesFunV2(distVar, sourVar, nameFile=''):
    """Function to find and replace required text part at given file
    distVar depicts finding variables
    sourVar depicts replacing variables
    nameFile is the name of file where the procedure will be done"""


    if os.path.isfile(nameFile):
        with open (nameFile, 'r') as f:
            oldData = f.read()
        newData = oldData.replace(str(distVar), str(sourVar))
        with open(nameFile, 'w') as f:
            f.write(newData)
    else:
        print(f'Warning: The file {nameFile} is not exist!')

def changeVariablesFun(distVar, sourVar, nameFile=' '):
    """The fucntion is devoted to change  gotten text part
    distVar is variable defended text, which should be replaced
    sourVar is variable defended text, which should be entered instead replaced text part
    nameFile is name of file where the procedure will be executed.
    """
    os.system("sed -i 's/{0}/{1}/g' {2}".format(distVar, sourVar, nameFile))
