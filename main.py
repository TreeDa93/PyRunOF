import os
from Modules.Manipulations import Manipulations

testPath = os.path.abspath('newTest')
basePath = '/home/ivan/openfoam/OpenFOAM-6/tutorials/incompressible/icoFoam/cavity/cavity'


if __name__ == "__main__":


    Manipulations().dublicateCase(baseCasePath=basePath, newPath=testPath, mode='rewrite')

    print(testPath)

